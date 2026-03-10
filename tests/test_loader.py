import pytest
from src.loader import TaskLoader
from src.sources import ApiStubTaskSource
from src.models import Task


class TestTaskLoader:
    def test_load_all(self):
        data = [{'id': '1', 'payload': 'A'}, {'id': '2', 'payload': 'B'}]
        source = ApiStubTaskSource(data)
        loader = TaskLoader(source)
        
        tasks = loader.load_all()
        
        assert len(tasks) == 2
        assert isinstance(tasks[0], Task)

    def test_loader_rejects_invalid_source(self):
        with pytest.raises(TypeError):
            TaskLoader("invalid") 