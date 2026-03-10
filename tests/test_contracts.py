import pytest
from src.contracts import TaskSource
from src.sources import validate_source, FileTaskSource, ApiStubTaskSource
from pathlib import Path
import tempfile
import json


class TestProtocolRuntimeCheck:

    def test_valid_source_is_instance(self):
        source = ApiStubTaskSource([{'id': 1, 'payload': {}}])
        assert isinstance(source, TaskSource)

    def test_invalid_source_is_not_instance(self):
        class BadSource:
            def fetch(self): pass
        
        assert not isinstance(BadSource(), TaskSource)

    def test_validate_source_success(self):
        source = ApiStubTaskSource([])
        result = validate_source(source)
        assert result is source

    def test_validate_source_failure(self):
        with pytest.raises(TypeError):
            validate_source("not a source")