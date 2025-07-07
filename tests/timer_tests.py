import pytest
from datetime import datetime, timedelta
from src.timer import Timer
from src.parser import CommandLineArgsParser
from src.writer import FakeFileWriter

parser = CommandLineArgsParser("5m", "This should finish in 5 minutes")

def validate_timer(timer):
    has_created_timer = timer.create()
    assert has_created_timer

def create_fake_file_writer():
    return FakeFileWriter(datetime.now())

def create_cmd_line_args_parser(time, desc):
    return CommandLineArgsParser(time, desc)

def create_default_cmd_line_args_parser():
    return create_cmd_line_args_parser("5m", "This should finish in 5 minutes")

def test_can_create_five_minute_timer():
    t = Timer(create_fake_file_writer())
    validate_timer(t)

def test_after_timer_created_should_not_be_active():
    t = Timer(create_fake_file_writer())
    validate_timer(t)
    assert not t.is_active()

def test_when_timer_is_started_should_be_active():
    t = Timer(create_fake_file_writer())
    validate_timer(t)
    t.start()
    assert t.is_active()

def test_timer_is_started_and_then_stopped_should_not_be_active():
    t = Timer(create_fake_file_writer())
    validate_timer(t)
    t.start()
    t.stop()
    assert not t.is_active()

def test_when_timer_is_started_fake_writer_should_return_write_amount_greater_than_zero():
    fake_writer = create_fake_file_writer()
    t = Timer(fake_writer)
    validate_timer(t)
    t.start()
    assert fake_writer.write_amount > 0

def test_when_timer_is_started_twice_without_stopping_fake_writer_should_contain_write_amount_equals_one():
    fake_writer = create_fake_file_writer()
    t = Timer(fake_writer)
    validate_timer(t)
    t.start()
    t.start()
    assert fake_writer.write_amount == 1

def test_when_timer_is_started_fake_writer_should_contain_non_empty_filename():
    fake_writer = create_fake_file_writer()
    t = Timer(fake_writer)
    validate_timer(t)
    t.start()
    assert fake_writer.returned_filename != ""

def test_when_timer_is_started_fake_writer_should_contain_filename_matching_parser():
    parser = create_default_cmd_line_args_parser()
    parser.process_args();

    curr_timestamp = parser.out_timestamp.current_timestamp
    fake_writer = FakeFileWriter(curr_timestamp)

    t = Timer(fake_writer)
    validate_timer(t)
    t.start()
    parser_filename = curr_timestamp.strftime("%Y%m%d_%H%M%S")
    assert fake_writer.returned_filename == parser_filename

