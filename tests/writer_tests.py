import pytest
from datetime import datetime, timedelta
from src.writer import FakeFileWriter

def test_can_call_write():
    w = FakeFileWriter(datetime.now())
    w.write()
    assert w.write_amount > 0

def test_write_is_called_has_valid_returned_filename():
    w = FakeFileWriter(datetime.now())
    w.write()
    assert w.returned_filename != ""
