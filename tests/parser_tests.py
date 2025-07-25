import pytest
from src.parser import CommandLineArgsParser, InvalidArgumentError

# Tests to make sure when "add" command is tested, then things behave as intended...
# e.g. "kt add -m 'Walk the dog.' -t 20m"

def test_given_invalid_command_line_arg_amount_should_throw_exception():
    invalid_parser = CommandLineArgsParser("-m", "test", "-m", "Additional messages not allowed.", "-t", "20s")

    with pytest.raises(InvalidArgumentError):
        invalid_parser.process_args()

def test_given_valid_command_line_arg_amount_should_not_throw_exception():
    parser = CommandLineArgsParser("-m", "Focus on work for 30 minutes", "-t", "30m")

    parsed_args = parser.process_args()
    assert parsed_args is not None

def test_given_no_arguments_should_throw_exception():
    invalid_parser = CommandLineArgsParser()
    
    with pytest.raises(InvalidArgumentError):
        invalid_parser.process_args()

def test_given_command_line_args_with_invalid_duration_should_throw_exception():
    invalid_parser = CommandLineArgsParser("-m", "test", "-t", "20ss")

    with pytest.raises(InvalidArgumentError):
        invalid_parser.process_args()

def test_given_command_line_args_with_duration_of_zero_should_not_throw_exception():
    invalid_parser = CommandLineArgsParser("-m", "test", "-t", "0s")

    parsed_args = invalid_parser.process_args()
    assert parsed_args is not None

def test_given_valid_command_line_args_with_args_count_of_two_should_not_throw_exception():
    parser = CommandLineArgsParser("-t", "20h")

    parsed_args = parser.process_args()
    assert parsed_args is not None

def test_given_invalid_command_line_args_with_args_count_of_two_should_not_throw_exception():
    invalid_parser = CommandLineArgsParser("-tt", "20h")

    with pytest.raises(InvalidArgumentError):
        invalid_parser.process_args()

    invalid_parser = CommandLineArgsParser("-t", "20hm")

    with pytest.raises(InvalidArgumentError):
        invalid_parser.process_args()

def test_given_invalid_command_line_args_with_args_count_of_four_should_not_throw_exception():
    invalid_parser = CommandLineArgsParser("-mm", "test", "-t" "20s")

    with pytest.raises(InvalidArgumentError):
        invalid_parser.process_args()

    invalid_parser = CommandLineArgsParser("-m", "test", "20ms")

    with pytest.raises(InvalidArgumentError):
        invalid_parser.process_args()
