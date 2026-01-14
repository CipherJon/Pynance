import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from file_organizer.config import LOG_CONFIG
from file_organizer.organizer import organize_files


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else getattr(logging, LOG_CONFIG["level"])

    # Ensure the log file directory exists and is writable
    log_file_path = Path(LOG_CONFIG["file"])
    if not log_file_path.parent.exists():
        try:
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(
                f"WARNING: Could not create log directory: {e}. Falling back to default location."
            )
            log_file_path = Path.home() / "file_organizer.log"

    # Check if the log file is writable
    try:
        with open(log_file_path, "a") as f:
            pass
    except Exception as e:
        print(
            f"WARNING: Could not write to log file: {e}. Falling back to default location."
        )
        log_file_path = Path.home() / "file_organizer.log"

    logging.basicConfig(
        level=level,
        format=LOG_CONFIG["format"],
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler(sys.stdout),
        ],
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Organize files in a directory based on file types and dates."
    )
    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        help="Directory to organize (default: ~/Downloads)",
    )
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=4,
        help="Number of worker threads (default: 4)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point for the file organizer."""
    args = parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        base_dir = Path(args.directory) if args.directory else None
        results = organize_files(base_dir, args.workers)

        # Print results
        if results["success"]:
            print("\nSuccessfully processed files:")
            for msg in results["success"]:
                print(f"✓ {msg}")

        if results["failed"]:
            print("\nFailed to process files:")
            for msg in results["failed"]:
                print(f"✗ {msg}")

        return 0

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
