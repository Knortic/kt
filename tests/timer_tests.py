import pytest
from datetime import datetime, timedelta
from src.timer import Timer
from src.parser import CommandLineArgsParser
from src.writer import FakeFileWriter

parser = CommandLineArgsParser("5m", "This should finish in 5 minutes")
fake_writer = FakeFileWriter(datetime.now())

def validate_timer(timer):
    has_created_timer = timer.create()
    assert has_created_timer

def test_can_create_five_minute_timer():
    t = Timer(parser, fake_writer)
    validate_timer(t)

def test_after_timer_created_should_not_be_active():
    t = Timer(parser, fake_writer)
    validate_timer(t)
    assert not t.is_active()

def test_when_timer_is_started_should_be_active():
    t = Timer(parser, fake_writer)
    validate_timer(t)
    t.start()
    assert t.is_active()

def test_timer_is_started_and_then_stopped_should_not_be_active():
    t = Timer(parser, fake_writer)
    validate_timer(t)
    t.start()
    t.stop()
    assert not t.is_active()

def test_when_timer_is_started_should_return_write_amount_greater_than_zero():
    t = Timer(parser, fake_writer)
    validate_timer(t)
    t.start()
    assert fake_writer.write_amount > 0

