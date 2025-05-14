from src.parser import CommandLineArgsParser

parser = CommandLineArgsParser()

def test_is_command_line_args_greater_than_zero():
    cmd_line_args = parser.fetch_args()
    assert len(cmd_line_args) > 0

def test_is_first_command_line_arg_a_number():
    cmd_line_args = parser.fetch_args()
    if cmd_line_args[0].isnumeric():
        assert True
    else:
        assert False
