import pytest
from src.parser import CommandLineArgsParser, InvalidArgumentError

parser = CommandLineArgsParser("0", "Focus on work for 30 minutes")

def test_is_command_line_args_greater_than_zero():
    args = parser.process_args()
    assert len(args) > 0

def test_is_first_command_line_arg_a_number():
    args = parser.process_args()
    assert args[0].isnumeric()

def test_given_command_line_arg_amount_above_two_should_throw_exception():
    invalid_parser = CommandLineArgsParser("0", "test", "invalid")

    with pytest.raises(InvalidArgumentError):
        invalid_parser.process_args()

def test_is_first_command_line_arg_positive():
    args = parser.process_args()
    assert(int(args[0]) >= 0)

def test_given_first_command_line_arg_negative_should_throw_exception():
    invalid_parser = CommandLineArgsParser("-1", "test")

    with pytest.raises(InvalidArgumentError):
        invalid_parser.process_args()

def test_given_first_command_line_arg_is_not_a_number_throw_exception():
    invalid_parser = CommandLineArgsParser("test", "test")

    with pytest.raises(InvalidArgumentError):
        invalid_parser.process_args()

def test_given_second_command_line_arg_is_not_a_string_throw_exception():
    invalid_parser = CommandLineArgsParser("0", 0)

    with pytest.raises(InvalidArgumentError):
        invalid_parser.process_args()

def test_first_argument_can_handle_minute_time_format():
    valid_parser = CommandLineArgsParser("30m", "Focus on work for 30 minutes")
    args = valid_parser.process_args()
    assert args[0].isnumeric()
    assert int(args[0]) == 30

