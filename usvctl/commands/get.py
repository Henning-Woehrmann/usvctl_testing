import typer
from rich.console import Console
from rich.table import Table
from .models.tasks import Tasks
from .models.rules import Rules


app = typer.Typer(help="Display one or many resources.")
console = Console()


api_address: str = None


@app.command("tasks")
def tasks():
    """
    Display tasks.
    """
    tasks_table = get_tasks_table()
    console.print(tasks_table)


@app.command("rules")
def rules():
    """
    Display rules.
    """
    rules_table = get_rules_table()
    console.print(rules_table)


def get_tasks_table(name: str = None, prefix: bool = False) -> Table:
    tasks = Tasks.get(api_address)

    table = Table("NAME", "ENABLED", "LABELS", "ENDPOINT", "ACTION")
    table.box = None

    for task in tasks.__root__:
        if name is None or name in task.metadata.name:
            table.add_row(
                ("task/" if prefix else "") + task.metadata.name,
                str(task.spec.enabled),
                str(task.metadata.labels),
                task.spec.endpoint,
                task.spec.action
            )

    return table


def get_rules_table(name: str = None, prefix: bool = False) -> Table:
    rules = Rules.get(api_address)

    table = Table("NAME", "ENABLED", "MATCHLABELS", "SOC")
    table.box = None

    for rule in rules.__root__:
        if name is None or name in rule.metadata.name:
            table.add_row(
                ("rule/" if prefix else "") + rule.metadata.name,
                str(rule.spec.enabled),
                str(rule.spec.selectors.matchLabels),
                str(rule.spec.condition.soc))

    return table
