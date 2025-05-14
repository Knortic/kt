import pytest
from src.timer import Timer
from src.parser import CommandLineArgsParser

def test_can_create_five_minute_timer():
    parser = CommandLineArgsParser("5m", "This should finish in 5 minutes")
    t = Timer(parser)
    has_created_timer = t.create()
    assert has_created_timer

def test_after_timer_created_should_not_be_active():
    parser = CommandLineArgsParser("5m", "This should finish in 5 minutes")
    t = Timer(parser)
    has_created_timer = t.create()
    assert has_created_timer
    assert not t.is_active()

