import asyncio
import openai
import json
from pathlib import Path
from typing import List

from .project import Project, ContentType, Platform, ProjectStatus
from .content_engine import GenerativeContentEngine
from .edit_engine import EditDecisionEngine
from .viral_engine import PredictiveViralEngine
from .export_system import ExportDeliverySystem
from .channel_manager import AutonomousChannelManager

class HollywoodEditor:
    """
    The main orchestrator for the entire autonomous video creation pipeline.
    """

    def __init__(self):
        """Initializes all the necessary engine components."""
        print("Initializing Hollywood Editor engines...")
        self.content_engine = GenerativeContentEngine()
        self.edit_engine = EditDecisionEngine()
        self.viral_engine = PredictiveViralEngine()
        self.export_system = ExportDeliverySystem()
        self.channel_manager = AutonomousChannelManager()
        print("✅ All engines ready.")

    async def _generate_voiceover(self, project: Project):
        """
        Generates a voiceover file and its word-level timestamps.
        The results are stored back into the project object.
        """
        print("🎤 Generating voiceover with timestamps...")
        output_dir = Path("./temp_audio")
        output_dir.mkdir(exist_ok=True)
        speech_file_path = output_dir / f"{project.project_id}_voiceover.mp3"

        try:
            # --- Request JSON to get timestamps ---
            response = await openai.audio.speech.acreate(
                model="tts-1-hd", # Using HD for better quality
                voice="alloy",
                input=project.script,
                response_format="json", # Request JSON to get timestamps
            )

            # The response content is a JSON string, parse it
            speech_json = json.loads(response.content)
            project.voiceover_timestamps = speech_json['words']

            # Now stream the audio data to a file
            audio_response = await openai.audio.speech.acreate(
                model="tts-1-hd",
                voice="alloy",
                input=project.script,
                response_format="mp3",
            )
            await audio_response.astream_to_file(speech_file_path)

            project.voiceover_file = speech_file_path
            print(f"✅ Voiceover and timestamps saved.")

        except Exception as e:
            print(f"❌ Failed to generate voiceover: {e}")
            project.voiceover_file = None
            project.voiceover_timestamps = None

    async def create_masterpiece(
        self,
        prompt: str,
        content_type: ContentType,
        target_platforms: List[Platform],
        target_duration: int = 30,
        source_files: List[str] = None,
        script: str = None,
    ) -> Project:
        """
        Runs the complete end-to-end pipeline to create a video.

        Args:
            prompt: The user's text prompt.
            content_type: The type of content to create.
            target_platforms: A list of platforms to export for.
            target_duration: The desired length of the video in seconds.
            source_files: Optional list of user-provided video files.
            script: Optional user-provided script.

        Returns:
            A completed Project object with status and output file paths.
        """
        project = Project(
            prompt=prompt,
            content_type=content_type,
            target_platforms=target_platforms,
            target_duration=target_duration,
            source_files=source_files or [],
            script=script,
        )

        try:
            # 1. Script Generation
            if not project.script:
                print(f"📝 Generating script for project {project.project_id}...")
                project.status = ProjectStatus.SCRIPTING
                project.script = await self.content_engine.generate_script(
                    project.prompt, project.content_type, project.target_duration
                )
                print("✅ Script generated.")

            # 2. Voiceover Generation (This method now handles both audio and timestamps)
            await self._generate_voiceover(project)

            # 3. Edit Decision
            print("🎬 Generating edit plan...")
            project.status = ProjectStatus.EDITING
            base_edl = self.edit_engine.generate_edit_plan(project)
            project.edit_decision_list = base_edl
            print("✅ Edit plan generated.")

            # 4. Viral Variants
            print("📈 Generating and scoring viral variants...")
            variants = self.viral_engine.generate_variants(base_edl, project)
            project.viral_variants = variants
            best_variant_id = self.viral_engine.select_best_variant(variants, project)
            best_variant = next(v for v in variants if v["id"] == best_variant_id)
            print(f"🏆 Selected best variant: '{best_variant['name']}'")

            # 5. Rendering
            print("🎥 Rendering final videos...")
            project.status = ProjectStatus.RENDERING
            for platform in project.target_platforms:
                output_path = self.export_system.render_video(
                    project, best_variant["edl"], platform
                )
                if output_path:
                    project.output_paths[platform.value] = output_path

            project.status = ProjectStatus.COMPLETE
            print(f"🎉 Project {project.project_id} complete!")

        except Exception as e:
            project.status = ProjectStatus.FAILED
            print(f"❌ An error occurred: {e}")

        return project

    def cleanup(self):
        """Cleans up temporary files generated during the process."""
        # In a real implementation, this would delete temp folders for
        # stock footage, audio, and render caches.
        print("🧹 Cleaning up temporary files...")
        # Placeholder for cleanup logic
        print("✅ Cleanup complete.")
