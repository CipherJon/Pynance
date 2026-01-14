import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from .config import LOG_CONFIG
from .organizer import organize_files


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else getattr(logging, LOG_CONFIG["level"])
    logging.basicConfig(
        level=level,
        format=LOG_CONFIG["format"],
        handlers=[
            logging.FileHandler(LOG_CONFIG["file"]),
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
