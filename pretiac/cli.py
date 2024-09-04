from argparse import ArgumentParser
from pprint import pprint

from pretiac import set_default_client
from pretiac.check_executor import check
from pretiac.config import load_config_file
from pretiac.log import logger


def main() -> None:
    client = set_default_client()
    parser = ArgumentParser(
        prog="icinga-api",
        description="Command line interface for the Icinga2 API.",
    )

    # global options
    parser.add_argument(
        "-d",
        "--debug",
        action="count",
        default=0,
        help="Increase debug verbosity (use up to 3 times): -d: info -dd: debug -ddd: verbose.",
    )

    sub_parsers = parser.add_subparsers(dest="sub_command", help="sub-command help")

    # check
    check_parser = sub_parsers.add_parser(
        "check", help="Execute checks and send it to the monitoring server."
    )

    check_parser.add_argument("--file")

    # config
    sub_parsers.add_parser("config", help="Dump the configuration")

    # send-service-check-result
    send_parser = sub_parsers.add_parser(
        "send-service-check-result",
        help="Send service check results to the specified API endpoint.",
    )

    send_parser.add_argument("service")

    send_parser.add_argument("--host")

    send_parser.add_argument("--exit-status")

    send_parser.add_argument("--plugin-output")

    send_parser.add_argument("--performance-data")

    # status
    sub_parsers.add_parser(
        "status",
        help="Retrieve status information and statistics for Icinga 2.",
    )

    args = parser.parse_args()

    logger.set_level(args.debug)
    logger.show_levels()

    if args.sub_command == "check":
        check(args.file)

    elif args.sub_command == "config":
        config = load_config_file()
        pprint(vars(config), indent=4)

    elif args.sub_command == "send-service-check-result":
        pprint(
            client.send_service_check_result(
                service=args.service,
                host=args.host,
                exit_status=args.exit_status,
                plugin_output=args.plugin_output,
                performance_data=args.performance_data,
            )
        )

    elif args.sub_command == "status":
        pprint(client.get_status(), indent=4)
