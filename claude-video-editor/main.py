#!/usr/bin/env python3
"""
Hollywood Editor CLI - Autonomous AI Video Creation Platform
Create, edit, and publish videos with a single command
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
import logging
from datetime import datetime

# Import the Hollywood Editor
from hollywood_editor import (
    HollywoodEditor,
    Project,
    ProjectStatus,
    Platform,
    ContentType
)

# Initialize Typer app
app = typer.Typer(
    name="Hollywood Editor",
    help="AI-powered autonomous video creation and channel management platform",
    add_completion=False
)

# Rich console for beautiful output
console = Console()

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ============================================================================
# CLI COMMANDS
# ============================================================================

@app.command()
def create(
    prompt: str = typer.Argument(..., help="Content prompt or topic for video generation"),
    video_path: Optional[str] = typer.Option(None, "--input", "-i", help="Optional input video file"),
    content_type: str = typer.Option("educational", "--type", "-t", help="Content type: educational, entertainment, tutorial, etc."),
    platforms: List[str] = typer.Option(["youtube"], "--platform", "-p", help="Target platforms (can specify multiple)"),
    duration: Optional[int] = typer.Option(None, "--duration", "-d", help="Target duration in seconds"),
    auto_publish: bool = typer.Option(False, "--publish", help="Automatically publish to platforms"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory for exports"),
    config_file: Optional[str] = typer.Option(None, "--config", "-c", help="Configuration file path"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """
    Create a video masterpiece from a simple prompt.
    
    The AI will:
    - Generate a script
    - Source relevant media
    - Create multiple viral variants
    - Edit with Hollywood-quality polish
    - Export for all target platforms
    - Optionally publish and track performance
    """
    
    # Show banner
    console.print(Panel.fit(
        "[bold cyan]🎬 HOLLYWOOD EDITOR[/bold cyan]\n"
        "[dim]Autonomous AI Video Creation Platform[/dim]",
        border_style="cyan"
    ))
    
    # Validate inputs
    try:
        content_type_enum = ContentType(content_type.lower())
    except ValueError:
        console.print(f"[red]Invalid content type: {content_type}[/red]")
        console.print("Valid types: educational, entertainment, tutorial, review, news, motivation, comedy, documentary")
        raise typer.Exit(1)
    
    platform_enums = []
    for p in platforms:
        try:
            platform_enums.append(Platform(p.lower()))
        except ValueError:
            console.print(f"[red]Invalid platform: {p}[/red]")
            console.print("Valid platforms: youtube, youtube_shorts, tiktok, instagram_reel, instagram_story, twitter, linkedin")
            raise typer.Exit(1)
    
    # Load configuration
    config = {}
    if config_file and Path(config_file).exists():
        with open(config_file) as f:
            config = json.load(f)
        console.print(f"[green]Loaded configuration from {config_file}[/green]")
    
    config["auto_publish"] = auto_publish
    
    # Set logging level
    if verbose:
        logging.getLogger().setLevel(logging.INFO)
    
    # Create project
    console.print(f"\n[bold]Creating video about:[/bold] {prompt}")
    console.print(f"[bold]Content type:[/bold] {content_type}")
    console.print(f"[bold]Target platforms:[/bold] {', '.join(platforms)}")
    if duration:
        console.print(f"[bold]Target duration:[/bold] {duration} seconds")
    
    # Run the async creation process
    asyncio.run(_create_video(
        prompt=prompt,
        video_path=video_path,
        content_type=content_type_enum,
        platforms=platform_enums,
        duration=duration,
        config=config,
        output_dir=output_dir
    ))

@app.command()
def status(
    project_id: str = typer.Argument(..., help="Project ID to check status")
):
    """Check the status of a video creation project."""
    
    # This would connect to a running Hollywood Editor instance
    # For now, check if project file exists
    project_file = Path(f"exports/{project_id}/{project_id}.json")
    
    if not project_file.exists():
        console.print(f"[red]Project {project_id} not found[/red]")
        raise typer.Exit(1)
    
    with open(project_file) as f:
        project_data = json.load(f)
    
    # Display status
    table = Table(title=f"Project {project_id}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Status", project_data.get("status", "Unknown"))
    table.add_row("Created", project_data.get("created_at", "Unknown"))
    table.add_row("Progress", f"{project_data.get('progress', 0) * 100:.1f}%")
    table.add_row("Current Phase", project_data.get("current_phase", "Unknown"))
    
    if "output_paths" in project_data:
        for platform, path in project_data["output_paths"].items():
            table.add_row(f"Output ({platform})", path)
    
    console.print(table)

@app.command()
def performance(
    project_id: str = typer.Argument(..., help="Project ID to check performance")
):
    """View performance metrics for a published video."""
    
    project_file = Path(f"exports/{project_id}/{project_id}.json")
    
    if not project_file.exists():
        console.print(f"[red]Project {project_id} not found[/red]")
        raise typer.Exit(1)
    
    with open(project_file) as f:
        project_data = json.load(f)
    
    if "performance_data" not in project_data:
        console.print("[yellow]No performance data available yet[/yellow]")
        raise typer.Exit(0)
    
    # Display performance metrics
    perf_data = project_data["performance_data"]
    
    for platform, metrics in perf_data.items():
        table = Table(title=f"{platform.upper()} Performance")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Views", f"{metrics.get('views', 0):,}")
        table.add_row("Likes", f"{metrics.get('likes', 0):,}")
        table.add_row("Comments", f"{metrics.get('comments', 0):,}")
        table.add_row("Shares", f"{metrics.get('shares', 0):,}")
        table.add_row("Retention Rate", f"{metrics.get('retention_rate', 0):.1%}")
        table.add_row("Avg View Duration", f"{metrics.get('average_view_duration', 0):.1f}s")
        
        console.print(table)
        console.print()

@app.command()
def batch(
    prompts_file: str = typer.Argument(..., help="JSON file containing multiple prompts"),
    platforms: List[str] = typer.Option(["youtube_shorts", "tiktok"], "--platform", "-p"),
    auto_publish: bool = typer.Option(False, "--publish", help="Automatically publish all videos"),
    parallel: int = typer.Option(1, "--parallel", help="Number of videos to create in parallel")
):
    """Create multiple videos from a batch file."""
    
    prompts_path = Path(prompts_file)
    if not prompts_path.exists():
        console.print(f"[red]Prompts file not found: {prompts_file}[/red]")
        raise typer.Exit(1)
    
    with open(prompts_path) as f:
        batch_data = json.load(f)
    
    prompts = batch_data.get("prompts", [])
    if not prompts:
        console.print("[red]No prompts found in file[/red]")
        raise typer.Exit(1)
    
    console.print(f"[bold]Creating {len(prompts)} videos[/bold]")
    
    # Process prompts
    asyncio.run(_batch_create(prompts, platforms, auto_publish, parallel))

@app.command()
def templates():
    """Show available content templates and examples."""
    
    templates = {
        "Educational": {
            "prompt": "Create a 30-second video about the benefits of meditation",
            "platforms": ["youtube_shorts", "tiktok"],
            "type": "educational"
        },
        "Tutorial": {
            "prompt": "How to tie a tie in 5 easy steps",
            "platforms": ["instagram_reel", "youtube"],
            "type": "tutorial"
        },
        "Entertainment": {
            "prompt": "Top 5 mind-blowing space facts",
            "platforms": ["tiktok", "youtube_shorts"],
            "type": "entertainment"
        },
        "Motivation": {
            "prompt": "Daily motivation: Why you should never give up",
            "platforms": ["instagram_reel", "linkedin"],
            "type": "motivation"
        },
        "Review": {
            "prompt": "iPhone 15 Pro Max: Is it worth the upgrade?",
            "platforms": ["youtube", "twitter"],
            "type": "review"
        }
    }
    
    console.print("[bold cyan]Available Templates:[/bold cyan]\n")
    
    for name, template in templates.items():
        console.print(f"[bold]{name}:[/bold]")
        console.print(f"  Prompt: {template['prompt']}")
        console.print(f"  Platforms: {', '.join(template['platforms'])}")
        console.print(f"  Type: {template['type']}")
        console.print()
    
    console.print("[dim]Use these as examples for your own prompts![/dim]")

@app.command()
def config():
    """Generate a sample configuration file."""
    
    sample_config = {
        "api_keys": {
            "openai": "your-openai-api-key",
            "elevenlabs": "your-elevenlabs-api-key",
            "pexels": "your-pexels-api-key"
        },
        "api_credentials": {
            "youtube": {
                "client_id": "your-client-id",
                "client_secret": "your-client-secret",
                "refresh_token": "your-refresh-token"
            },
            "tiktok": {
                "access_token": "your-access-token"
            },
            "instagram": {
                "username": "your-username",
                "password": "your-password"
            }
        },
        "export_settings": {
            "quality": "high",
            "gpu_acceleration": True
        },
        "content_settings": {
            "default_duration": 30,
            "watermark": False,
            "branding": {
                "logo_path": "/path/to/logo.png",
                "outro_video": "/path/to/outro.mp4"
            }
        }
    }
    
    config_path = Path("hollywood_config.json")
    with open(config_path, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    console.print(f"[green]Sample configuration saved to: {config_path}[/green]")
    console.print("[yellow]Remember to add your actual API keys![/yellow]")

# ============================================================================
# ASYNC FUNCTIONS
# ============================================================================

async def _create_video(prompt: str, video_path: Optional[str], content_type: ContentType,
                       platforms: List[Platform], duration: Optional[int], 
                       config: dict, output_dir: Optional[str]):
    """Async function to create a video"""
    
    # Initialize Hollywood Editor
    editor = HollywoodEditor(config)
    
    # Create progress display
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        
        # Add main task
        task = progress.add_task("Creating masterpiece...", total=100)
        
        # Update callback
        def update_progress(project: Project):
            progress.update(task, 
                          completed=int(project.progress * 100),
                          description=project.current_phase or "Processing...")
        
        try:
            # Create the video
            project = await editor.create_masterpiece(
                video_path=video_path,
                prompt=prompt,
                content_type=content_type,
                target_platforms=platforms,
                target_duration=duration
            )
            
            # Update progress periodically
            while project.status not in [ProjectStatus.COMPLETE, ProjectStatus.FAILED]:
                await asyncio.sleep(1)
                current_project = editor.get_project_status(project.project_id)
                if current_project:
                    update_progress(current_project)
            
            progress.update(task, completed=100)
            
            # Show results
            if project.status == ProjectStatus.COMPLETE:
                console.print("\n[bold green]✨ Masterpiece created successfully![/bold green]")
                
                # Display output files
                if project.output_paths:
                    console.print("\n[bold]Output files:[/bold]")
                    for platform, path in project.output_paths.items():
                        console.print(f"  • {platform}: {path}")
                
                # Display publishing URLs
                if project.published_urls:
                    console.print("\n[bold]Published to:[/bold]")
                    for platform, url in project.published_urls.items():
                        console.print(f"  • {platform}: {url}")
                
                console.print(f"\n[bold]Project ID:[/bold] {project.project_id}")
                console.print("[dim]Use 'hollywood status <project-id>' to check progress[/dim]")
                console.print("[dim]Use 'hollywood performance <project-id>' to view metrics[/dim]")
                
            else:
                console.print("\n[bold red]❌ Creation failed![/bold red]")
                if project.errors:
                    console.print("[red]Errors:[/red]")
                    for error in project.errors:
                        console.print(f"  • {error['error']}")
        
        except Exception as e:
            console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
            raise typer.Exit(1)
        
        finally:
            # Cleanup
            editor.cleanup()

async def _batch_create(prompts: List[dict], platforms: List[str], 
                       auto_publish: bool, parallel: int):
    """Create multiple videos in batch"""
    
    platform_enums = [Platform(p.lower()) for p in platforms]
    
    # Create semaphore for parallel processing
    semaphore = asyncio.Semaphore(parallel)
    
    async def create_one(prompt_data: dict, index: int):
        async with semaphore:
            console.print(f"\n[bold]Creating video {index + 1}/{len(prompts)}[/bold]")
            
            editor = HollywoodEditor({"auto_publish": auto_publish})
            
            try:
                project = await editor.create_masterpiece(
                    prompt=prompt_data["prompt"],
                    content_type=ContentType(prompt_data.get("type", "educational")),
                    target_platforms=platform_enums,
                    target_duration=prompt_data.get("duration", 30)
                )
                
                if project.status == ProjectStatus.COMPLETE:
                    console.print(f"[green]✓ Video {index + 1} complete: {project.project_id}[/green]")
                else:
                    console.print(f"[red]✗ Video {index + 1} failed[/red]")
                
                return project
                
            except Exception as e:
                console.print(f"[red]Error creating video {index + 1}: {str(e)}[/red]")
                return None
            
            finally:
                editor.cleanup()
    
    # Create all videos
    tasks = [create_one(prompt_data, i) for i, prompt_data in enumerate(prompts)]
    results = await asyncio.gather(*tasks)
    
    # Summary
    successful = sum(1 for r in results if r and r.status == ProjectStatus.COMPLETE)
    console.print(f"\n[bold]Batch complete![/bold]")
    console.print(f"Successfully created: {successful}/{len(prompts)} videos")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    app()

if __name__ == "__main__":
    main()