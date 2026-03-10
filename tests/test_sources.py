import pytest
import json
import tempfile
from pathlib import Path
from src.sources import FileTaskSource, GeneratorTaskSource, ApiStubTaskSource
from src.models import Task


class TestFileTaskSource:
    def test_load_from_file(self):
        data = [{"id": "1", "payload": {"key": "value"}}]
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as f:
            json.dump(data, f)
            path = Path(f.name)
        
        source = FileTaskSource(path)
        tasks = list(source.get_task())
        
        assert len(tasks) == 1
        assert tasks[0].id == "1"
        path.unlink()

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as f:
            json.dump([], f)
            path = Path(f.name)
        
        source = FileTaskSource(path)
        tasks = list(source.get_task())
        
        assert len(tasks) == 0
        path.unlink()


class TestGeneratorTaskSource:
    def test_load_from_generator(self):
        def gen():
            yield {'id': 10, 'payload': 'test'}
            yield {'id': 11, 'payload': 'test2'}
        
        source = GeneratorTaskSource(gen())
        tasks = list(source.get_task())
        
        assert len(tasks) == 2
        assert tasks[0].id == "10"


class TestApiStubTaskSource:
    def test_load_stub(self):
        data = [{'id': 'api_1', 'payload': None}]
        source = ApiStubTaskSource(data)
        tasks = list(source.get_task())
        
        assert tasks[0].id == 'api_1'