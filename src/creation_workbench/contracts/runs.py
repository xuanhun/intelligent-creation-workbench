"""Legal Run state edges, independent of Codex Turn states.

Business completion checks and persistence belong to the application service.
"""

from enum import StrEnum


class RunState(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    WAITING_EXTERNAL = "waiting_external"
    NEEDS_REVIEW = "needs_review"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class InvalidTransition(ValueError):
    """The requested edge is not part of the business state graph."""


_EDGES = {
    RunState.CREATED: frozenset({RunState.RUNNING, RunState.CANCELLED}),
    RunState.RUNNING: frozenset({
        RunState.WAITING_EXTERNAL, RunState.NEEDS_REVIEW,
        RunState.FAILED, RunState.CANCELLED,
    }),
    RunState.WAITING_EXTERNAL: frozenset({
        RunState.RUNNING, RunState.FAILED, RunState.CANCELLED,
    }),
    RunState.NEEDS_REVIEW: frozenset({
        RunState.RUNNING, RunState.COMPLETED, RunState.CANCELLED,
    }),
    RunState.COMPLETED: frozenset(),
    RunState.FAILED: frozenset(),
    RunState.CANCELLED: frozenset(),
}


def transition(current: RunState, target: RunState) -> RunState:
    """Validate a state edge, without mutating or persisting a Run.

    CREATED -> CANCELLED permits cancelling a queued run before execution.
    Duplicate command handling belongs to the future idempotent service.
    """
    current, target = RunState(current), RunState(target)
    if target not in _EDGES[current]:
        raise InvalidTransition(f"Cannot transition {current.value} -> {target.value}")
    return target
