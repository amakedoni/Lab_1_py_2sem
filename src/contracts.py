from typing import Protocol, runtime_checkable, Iterable
from .models import Task

@runtime_checkable
class TaskSource(Protocol):

	def get_task(self) -> Iterable[Task]:
		...