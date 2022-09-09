# source: https://github.com/tiangolo/typer/issues/310

import typer

from .exceptions import APIError
from httpx import ConnectError


ERROR_COLOR = typer.colors.BRIGHT_RED


class ErrorHandlingTyper(typer.Typer):

    def __call__(self, *args, **kwargs):
        try:
            super(ErrorHandlingTyper, self).__call__(*args, **kwargs)
        except APIError as e:
            typer.secho(e, fg=ERROR_COLOR)
        except ConnectError:
            typer.secho("Could not connect to the usv-controller. Please check the api-address", fg=ERROR_COLOR)
        except Exception as e:
            error_type = typer.style(type(e).__name__ + ":", fg=ERROR_COLOR)
            typer.echo(error_type + " " + str(e))
