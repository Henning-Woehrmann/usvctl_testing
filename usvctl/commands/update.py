import typer
from typing import List
from pydantic import BaseModel
from rich import print_json

from .models.tasks import Task
from .models.rules import Rule

app = typer.Typer(help="Update a resource.")

api_address: str = None


@app.command()
def task(
        name: str = typer.Argument(..., help="The name of the task"),
        endpoint: str = typer.Option(None, help="The endpoint of idk..."),
        action: str = typer.Option(None, help="Name of the script to execute when task get's called"),
        test: str = typer.Option(None, help="Name of the test script"),
        healthcheck: str = typer.Option(None, help="Name of the script for the healthcheck"),
        label: List[str] = typer.Option(None, help="Enter labels \"foo=bar abc=def)\""),
        enabled: bool = typer.Option(None, "--enabled/--not-enabled", help="Enable the task on creation")):
    """
    Update a task.
    """
    if len(label) > 0:
        labels = {x.split('=')[0]: x.split('=')[1] for x in label}  # Parse list into dict
    else:
        labels = None

    task = Task.get(api_address, name)

    if endpoint is not None:
        task.spec.endpoint = endpoint
    if action is not None:
        task.spec.action = action
    if test is not None:
        task.spec.test = test
    if healthcheck is not None:
        task.spec.healthcheck = healthcheck
    if labels is not None:
        task.metadata.labels = labels
    if enabled is not None:
        task.spec.enabled = enabled

    confirm_and_send(task)


@app.command()
def rule(
        name: str = typer.Argument(..., help="The name of the task"),
        soc: int = typer.Option(None, help=""),
        match_label: List[str] = typer.Option(None, help="Enter labels \"foo=bar\""),
        enabled: bool = typer.Option(False, "--enabled/--not-enabled", help="Enable the task on creation")):
    """
    Update a rule.
    """
    if len(match_label) > 0:
        match_labels = {x.split('=')[0]: x.split('=')[1] for x in match_label}
    else:
        match_labels = None

    rule = Rule.get(api_address, name)

    if match_labels is not None:
        rule.spec.selectors.matchLabels = match_labels
    if soc is not None:
        rule.spec.condition.soc = soc
    if enabled is not None:
        rule.spec.enabled = enabled

    confirm_and_send(rule)


def confirm_and_send(resource_object: BaseModel):

    print_json(resource_object.json())

    confirm = typer.confirm(f"Are you sure you want to update this {resource_object.__class__.__name__.lower()}?")
    if confirm:
        resource_object.update(api_address)
    else:
        raise typer.Abort()
