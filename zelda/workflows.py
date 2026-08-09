from dataclasses import dataclass, field
from typing import Callable

from zelda.events.bus import Event, EventBus


@dataclass
class WorkflowStep:
    name: str
    handler: Callable[[dict], dict]


@dataclass
class Workflow:
    name: str
    steps: list[WorkflowStep] = field(default_factory=list)

    def run(self, context: dict) -> dict:
        current = dict(context)
        for step in self.steps:
            current.update(step.handler(current))
        return current


class WorkflowEngine:
    """Runs explicitly registered workflows. No arbitrary code is accepted as a step."""

    def __init__(self, event_bus: EventBus) -> None:
        self.event_bus = event_bus
        self.workflows: dict[str, Workflow] = {}

    def register(self, workflow: Workflow) -> None:
        if workflow.name in self.workflows:
            raise ValueError(f"Workflow already registered: {workflow.name}")
        self.workflows[workflow.name] = workflow

    def trigger(self, name: str, context: dict | None = None) -> dict:
        workflow = self.workflows.get(name)
        if workflow is None:
            raise KeyError(f"Unknown workflow: {name}")
        result = workflow.run(context or {})
        self.event_bus.publish(Event("workflow.completed", {"workflow": name, "result": result}))
        return result
