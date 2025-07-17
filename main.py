# main.py
# The main entry point for our Autonomous Video Editor.

import argparse
import sys
import os

# We will build these modules next. This structure allows for a clean,
# scalable, and professional architecture.
from editor import Editor
from config import STYLE_PROFILES, get_default_style


def main():
    """
    Orchestrates the entire video editing process from the command line.

    This function parses user input, validates paths, instantiates the main
    Editor object, and kicks off the editing pipeline. It's the "engine start"
    button for the whole application.
    """
    parser = argparse.ArgumentParser(
        description="Autonomous Video Editor powered by AI.",
        # Allows for better help text formatting with newlines
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "video_path",
        type=str,
        help="The absolute path to the input video file."
    )

    parser.add_argument(
        "--style",
        type=str,
        default=get_default_style(),
        choices=STYLE_PROFILES.keys(),
        help="The editing style to apply. Defines the 'taste' of the AI Director.\n"
             f"Available styles: {', '.join(STYLE_PROFILES.keys())}"
    )

    parser.add_argument(
        "--output_path",
        type=str,
        default=None,
        help="Optional: The path to save the final edited video.\n"
             "If not provided, it will be saved next to the original with an '_edited' suffix."
    )

    args = parser.parse_args()

    # --- Input Validation ---
    if not os.path.isfile(args.video_path):
        print(f"Error: The file '{args.video_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print("--- Autonomous Video Editor Initialized ---")
    try:
        # This is the core action. We hand off control to the Editor class.
        editor_instance = Editor(
            video_path=args.video_path,
            style_name=args.style,
            output_path=args.output_path
        )
        editor_instance.run_pipeline()

        print("\n✅ Success! Editing pipeline completed.")
        print(f"Final video saved to: {editor_instance.project.output_path}")

    except Exception as e:
        # A robust catch-all for any errors during the complex editing process.
        print(f"\n❌ An unexpected error occurred: {e}", file=sys.stderr)
        # For developers, printing the full traceback is invaluable for debugging.
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()