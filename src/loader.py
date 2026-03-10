from .models import Task
from .contracts import TaskSource
from .sources import validate_source

class TaskLoader: 

	def __init__(self, source: TaskSource):
		self._source = validate_source(source)
	
	def load_all(self) -> list[Task]:
		return list(self._source.get_task())