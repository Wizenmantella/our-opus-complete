# main.py
import argparse
import sys
import os
from editor import Editor
from config import STYLE_PROFILES, get_default_style

def main():
    """
    The main entry point for the Autonomous Video Editor.
    """
    parser = argparse.ArgumentParser(
        description="Autonomous Video Editor - Forged by The Agency.",
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

    if not os.path.isfile(args.video_path):
        print(f"Error: The file '{args.video_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print("--- Autonomous Video Editor Initialized ---")
    try:
        editor_instance = Editor(
            video_path=args.video_path,
            style_name=args.style,
            output_path=args.output_path
        )
        editor_instance.run_pipeline()
        print("--- Video Editing Complete ---")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()