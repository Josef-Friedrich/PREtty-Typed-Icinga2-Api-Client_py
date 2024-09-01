from argparse import ArgumentParser
from pprint import pprint

from pretiac import get_status, send_service_check_result
from pretiac.config import load_config


def main() -> None:
    parser = ArgumentParser(
        prog="icinga-api",
        description="Command line interface for the Icinga2 API.",
    )

    sub_parsers = parser.add_subparsers(dest="sub_command", help="sub-command help")

    sub_parsers.add_parser("config", aliases=("c"), help="Dump the configuration")

    send_parser = sub_parsers.add_parser(
        "send-service-check-result",
        aliases=("s", "send", "send-service"),
        help="Send / Process service check results to the specified API endpoint.",
    )

    send_parser.add_argument("service")

    send_parser.add_argument("--host")

    send_parser.add_argument("--exit-status")

    send_parser.add_argument("--plugin-output")

    send_parser.add_argument("--performance-data")

    sub_parsers.add_parser(
        "status",
        aliases=("st"),
        help="Retrieve status information and statistics for Icinga 2.",
    )

    args = parser.parse_args()

    if args.sub_command in ("s", "send", "send-service"):
        args.sub_command = "send-service-check-result"

    if args.sub_command == "config":
        config = load_config()
        pprint(vars(config), indent=4)
    elif args.sub_command == "status":
        pprint(get_status(), indent=4)
    elif args.sub_command == "send-service-check-result":
        pprint(
            send_service_check_result(
                service=args.service,
                host=args.host,
                exit_status=args.exit_status,
                plugin_output=args.plugin_output,
                performance_data=args.performance_data,
            )
        )
