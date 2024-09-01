from argparse import ArgumentParser
from pprint import pprint

from pretiac import get_status
from pretiac.config import load_config


def main() -> None:
    parser = ArgumentParser(
        prog="icinga-api",
        description="Command line interface for the Icinga2 API.",
    )

    sub_parsers = parser.add_subparsers(dest="sub_command", help="sub-command help")

    sub_parsers.add_parser("config", aliases=("c"), help="Dump the configuration")

    sub_parsers.add_parser(
        "send-check-result",
        aliases=("s", "send"),
        help="Send / Process check results to the specified API endpoint.",
    )

    sub_parsers.add_parser(
        "status",
        aliases=("st"),
        help="Retrieve status information and statistics for Icinga 2.",
    )

    args = parser.parse_args()

    if args.sub_command == "config":
        config = load_config()
        pprint(vars(config), indent=4)
    elif args.sub_command == "status":
        pprint(get_status(), indent=4)

    print(args)
