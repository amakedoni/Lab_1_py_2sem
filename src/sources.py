import json
from pathlib import Path
from typing import Iterator, Any, List
from .models import Task
from .contracts import TaskSource

class FileTaskSource: 

	def __init__(self, file_path: Path):
		self.file_path = file_path

	def get_task(self) -> Iterator[Task]:
		with open(self.file_path, 'r', encoding='utf-8') as f:
			data = json.load(f)

			if isinstance(data, List):
				for item in data:
					yield Task(id=item['id'], payload=item['payload'])

class GeneratorTaskSource:

	def __init__(self, data_generator: Iterator[dict]):
		self._generator = data_generator

	def get_task(self) -> Iterator[Task]:
		for item in self._generator:
			yield Task(id=str(item['id']), payload=item.get('payload'))

class ApiStubTaskSource:

	def __init__(self, task_data: List[dict]):
		self._task_data = task_data

	def get_task(self) -> Iterator[Task]:
		for item in self._task_data:
			yield Task(id=item['id'], payload=item['payload'])

def validate_source(source: Any) -> TaskSource:

	if not isinstance(source, TaskSource):
		raise TypeError(f"Обьект {type(source)} не реализкет протокол TaskSource")

	return source

