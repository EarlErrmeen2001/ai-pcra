"""This script file prints test messages to verify the CLI tool functionality (whether it works correctly)."""

import argparse
import logging


def main():
    """Parse CLI arguments and log a message at the specified log level."""
    parser = argparse.ArgumentParser(
        description="CLI tool test script to print custom messages."
    )
    parser.add_argument(
        "--message",
        type=str,
        default="This is a test message from the CLI tool.",
        help="The message to log",
    )
    parser.add_argument(
        "--level",
        type=str,
        choices=["debug", "info", "warning", "error", "critical"],
        default="info",
        help="Logging level for the message",
    )

    args = parser.parse_args()

    # Configuration logging
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    log_func = getattr(logging, args.level.lower(), logging.info)
    log_func(args.message)


if __name__ == "__main__":
    main()
