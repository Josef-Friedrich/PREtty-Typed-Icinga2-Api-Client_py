from typing import Optional

import click
from rich import print

from pretiac import get_default_client
from pretiac.check_executor import check as execute_check
from pretiac.config import load_config_file
from pretiac.log import logger
from pretiac.object_types import (
    normalize_to_plural_snake_object_type_name,
)


@click.group()
@click.option(
    "-d",
    "--debug",
    count=True,
    help="Increase debug verbosity (use up to 3 times): -d: info -dd: debug -ddd: verbose.",
)
def main(debug: int) -> None:
    """Command line interface for the Icinga2 API."""
    logger.set_level(debug)
    logger.show_levels()


# v1/objects ###########################################################################


@click.group(invoke_without_command=True)
@click.argument("object_type")
def objects(object_type: str) -> None:
    """List the different configuration object types."""
    client = get_default_client()
    print(
        getattr(
            client,
            f"get_{normalize_to_plural_snake_object_type_name(object_type)}",
        )()
    )


# v1/actions ###########################################################################


@click.group(invoke_without_command=True)
def actions() -> None:
    """Subscribe to an event stream."""
    for event in get_default_client().subscribe_events(["CheckResult"], "cli"):
        print(event)


@click.command
@click.option("--plugin-output")
@click.option("--performance-data")
@click.option("--exit-status")
@click.option("--host")
@click.argument("service")
def send_service_check_result(
    service: str,
    host: Optional[str] = None,
    exit_status: Optional[str] = None,
    performance_data: Optional[str] = None,
    plugin_output: Optional[str] = None,
) -> None:
    """Send service check results to the specified API endpoint."""
    print(
        get_default_client().send_service_check_result(
            service=service,
            host=host,
            exit_status=1,
            plugin_output=performance_data,
            performance_data=plugin_output,
        )
    )


actions.add_command(send_service_check_result)


# v1/events ############################################################################


@click.command()
def events() -> None:
    """Subscribe to an event stream."""
    for event in get_default_client().subscribe_events(["CheckResult"], "cli"):
        print(event)


# v1/status ############################################################################


@click.command()
def status() -> None:
    """Retrieve status information and statistics for Icinga 2."""
    print(get_default_client().get_status())


# v1/config ############################################################################


@click.group(invoke_without_command=True)
@click.pass_context
def config(ctx: click.Context) -> None:
    if ctx.invoked_subcommand is None:
        print(get_default_client().list_all_config_stage_files())
        click.echo("Use a subcommand")


@click.command()
def config_show() -> None:
    print(get_default_client().list_all_config_stage_files())


@click.argument("stage", required=False)
@click.argument("package")
@click.command()
def config_delete(package: str, stage: Optional[str] = None) -> None:
    print(get_default_client().delete_config(package, stage))


config.add_command(config_delete, "delete")
config.add_command(config_show, "show")


# v1/types #############################################################################


@click.command()
def types() -> None:
    print(get_default_client().get_types())


# v1/variables #########################################################################


@click.command()
def variables() -> None:
    print(get_default_client().get_variables())


# other ################################################################################


@click.command()
@click.argument("file")
def check(file: str) -> None:
    """Execute checks and send it to the monitoring server."""
    execute_check(file)


@click.command()
def dump_config() -> None:
    """Dump the configuration of the pretiac client"""
    print(load_config_file())


main.add_command(objects)
main.add_command(actions)
main.add_command(events)
main.add_command(status)
main.add_command(config)
main.add_command(types)
main.add_command(variables)
main.add_command(check)
main.add_command(dump_config)
