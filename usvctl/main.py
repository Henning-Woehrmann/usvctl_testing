from .error_handling_typer import ErrorHandlingTyper
import typer
from .commands import create, delete, get, update

api_path: str = None

app = ErrorHandlingTyper(help="usvctl controls an specified usv-controller via the api of that controller")

app.add_typer(create.app, name="create")
app.add_typer(delete.app, name="delete")
app.add_typer(get.app, name="get")
app.add_typer(update.app, name="update")


@app.callback()
def callback(
        api: str = typer.Argument(... , help="Address of the api from the usv-controller [e.g. '10.20.30.40:8000']")):
    """
    This is a callback command ???
    """
    # TODO: Check, if addres is given with the prefix 'http://' or without
    # TODO: If usv-controller runs on same port always, check if port is given and use standard port if not
    # TODO: Use standard address, if no address is given
    api_address = f"http://{api}"

    create.api_address = api_address
    delete.api_address = api_address
    get.api_address = api_address
    update.api_address = api_address


# @app.error_handler(Exception)
# def handle_pydantic_error(e):
#     print(e)
#     return 2


if __name__ == "__main__":
    app()
