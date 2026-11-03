"""No concrete runtime is enabled until G0 compatibility acceptance."""

from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class RuntimeBinding:
    workspace_id: str
    conversation_id: str
    thread_id: str


@dataclass(frozen=True)
class RuntimeEvent:
    """Transient adapter event, not the future durable business SSE envelope."""

    type: str
    thread_id: str
    turn_id: str | None
    text: str | None = None


class RuntimeAdapter(Protocol):
    async def start(self, workspace_id: str, conversation_id: str) -> RuntimeBinding: ...

    async def resume(self, binding: RuntimeBinding) -> None: ...

    async def start_turn(self, binding: RuntimeBinding, prompt: str) -> str: ...

    async def steer(self, binding: RuntimeBinding, turn_id: str, prompt: str) -> None: ...

    async def interrupt(self, binding: RuntimeBinding, turn_id: str) -> None: ...

    def subscribe(self, binding: RuntimeBinding) -> AsyncIterator[RuntimeEvent]: ...

    async def shutdown(self) -> None: ...
