from typing import Optional

import click
from rich import print

from pretiac import get_default_client


@click.group()
def main() -> None:
    pass


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


@click.command()
def types() -> None:
    print(get_default_client().get_types())


@click.command()
def variables() -> None:
    print(get_default_client().get_variables())


@click.command()
def status() -> None:
    print(get_default_client().get_status())


main.add_command(config)
main.add_command(types)
main.add_command(variables)
main.add_command(status)
