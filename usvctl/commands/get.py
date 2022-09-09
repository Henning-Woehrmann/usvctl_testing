import typer
from rich.console import Console
from rich.table import Table
from .models.tasks import Tasks
from .models.rules import Rules
from .models.jobs import Jobs


app = typer.Typer(help="Display one or many resources.")
console = Console()


api_address: str = None


@app.command("all")
def all():
    """
    Display all resources
    """
    tasks_table = get_tasks_table(prefix=True)
    rules_table = get_rules_table(prefix=True)
    jobs_table = get_jobs_table(prefix=True)

    console.print(tasks_table)
    console.print()
    console.print(rules_table)
    console.print()
    console.print(jobs_table)


@app.command("tasks")
@app.command("task")
def tasks(name: str = typer.Argument(None, help="Filter the list by name (Part of the name is sufficient)")):
    """
    Display tasks.
    """
    tasks_table = get_tasks_table(name)
    console.print(tasks_table)


@app.command("rules")
@app.command("rule")
def rules(name: str = typer.Argument(None, help="Filter the list by name (Part of the name is sufficient)")):
    """
    Display rules.
    """
    rules_table = get_rules_table(name)
    console.print(rules_table)


@app.command("jobs")
@app.command("job")
def jobs(uuid: str = typer.Argument(None, help="Filter the list by uuid (Beginning of the uuid is sufficient)")):
    """
    Display jobs.
    """
    jobs_table = get_jobs_table(uuid)
    console.print(jobs_table)


def get_tasks_table(name: str = None, prefix: bool = False) -> Table:
    tasks = Tasks.get(api_address)

    table = Table("NAME", "ENABLED", "LABELS", "ENDPOINT")
    table.box = None

    for task in tasks.__root__:
        if name is None or name in task.metadata.name:
            table.add_row(
                ("task/" if prefix else "") + task.metadata.name,
                str(task.spec.enabled),
                str(task.metadata.labels),
                task.spec.endpoint
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


def get_jobs_table(uuid: str = None, prefix: bool = False) -> Table:
    jobs = Jobs.get(api_address)

    table = Table("UUID", "ENABLED", "STATE", "TASK", "RULE", "TASK_ENABLED", "RULE_ENABLED")
    table.box = None

    for job in jobs.__root__:
        if uuid is None or job.metadata.uuid.startswith(uuid):
            table.add_row(
                ("job/" if prefix else "") + job.metadata.uuid,
                str(job.status.enabled),
                job.status.state,
                job.metadata.labels.task,
                job.metadata.labels.rule,
                str(job.status.task_enabled),
                str(job.status.rule_enabled))

    return table
