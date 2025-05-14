from src.parser import CommandLineArgsParser

def test_is_command_line_args_greater_than_zero():
    parser = CommandLineArgsParser()
    cmd_line_args = parser.fetch_args()
    assert len(cmd_line_args) > 0
