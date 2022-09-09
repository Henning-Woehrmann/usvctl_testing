import typer
from rich import print_json

from .models.tasks import Task
from .models.rules import Rule

app = typer.Typer(help="Delete a resource.")

api_address: str = None


@app.command("task")
def task(name: str = typer.Argument(None, help="Name of the task to delete")):
    """
    Delete a task.
    """
    delete_resource(Task, name)


@app.command()
def rule(name: str = typer.Argument(None, help="Name of the rule to delete")):
    """
    Delete a rule.
    """
    delete_resource(Rule, name)


def delete_resource(resource_class, name: str):
    resource = resource_class.get(api_address, name)

    print_json(resource.json())

    confirm = typer.confirm(f"Are you sure you want to delete the {resource_class.__name__.lower()} shown above?")
    if confirm:
        resource.delete(api_address)
    else:
        raise typer.Abort()
