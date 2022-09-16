import typer
from typing import List
from rich import print_json
from pydantic import BaseModel

from .models.tasks import Task, Spec as TaskSpec, Metadata as TaskMetadata
from .models.rules import (
    Rule,
    Spec as RuleSpec,
    Metadata as RuleMetadata,
    Selectors as RuleSelectors,
    Condition as RuleCondition
)


app = typer.Typer(help="Create a new resource.")

api_address: str = None


@app.command()
def task(
        name: str = typer.Argument(..., help="The name of the task"),
        endpoint: str = typer.Option(..., help="The endpoint of idk..."),
        action: str = typer.Option(..., help="Name of the script to execute when task get's called"),
        test: str = typer.Option("", help="Name of the test script"),
        healthcheck: str = typer.Option("", help="Name of the script for the healthcheck"),
        label: List[str] = typer.Option(None, help="Enter labels \"--label foo=bar --label abc=def)\""),
        enabled: bool = typer.Option(False, help="Enable the task on creation")):
    """
    Create a new task.
    """
    labels = {x.split('=')[0]: x.split('=')[1] for x in label}  # Parse list into dict

    task = Task(
        metadata=TaskMetadata(
            name=name,
            labels=labels),
        spec=TaskSpec(
            enabled=enabled,
            endpoint=endpoint,
            action=action,
            test=test,
            healthcheck=healthcheck)
    )

    confirm_and_send(task)


@app.command()
def rule(
        name: str = typer.Argument(..., help="The name of the task"),
        match_label: List[str] = typer.Option(None, help="Enter labels \"foo=bar\""),
        enabled: bool = typer.Option(False, help="Enable the task on creation"),
        soc: int = typer.Option(0, help="")):
    """
    Create a new rule.
    """
    match_labels = {x.split('=')[0]: x.split('=')[1] for x in match_label}  # Parse list into dict

    rule = Rule(
        metadata=RuleMetadata(
            name=name,
        ),
        spec=RuleSpec(
            enabled=enabled,
            selectors=RuleSelectors(
                matchLabels=match_labels
            ),
            condition=RuleCondition(
                soc=soc
            )
        )
    )

    confirm_and_send(rule)


def confirm_and_send(resource_object: BaseModel):
    print_json(resource_object.json())

    confirmed = typer.confirm(f"Are you sure you want to create this {resource_object.__class__.__name__.lower()}?")

    if confirmed:
        resource_object.create(api_address)
    else:
        typer.Abort()
