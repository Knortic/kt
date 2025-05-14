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

def test_is_second_command_line_arg_a_string():
    args = parser.process_args()
    assert isinstance(args[1], str)

