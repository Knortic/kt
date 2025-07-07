import pytest
from datetime import datetime, timedelta
from src.timer import Timer
from src.parser import CommandLineArgsParser
from src.writer import FakeFileWriter

parser = CommandLineArgsParser("5m", "This should finish in 5 minutes")

def create_cmd_line_args_parser(time, desc):
    return CommandLineArgsParser(time, desc)

def create_default_cmd_line_args_parser():
    return create_cmd_line_args_parser("5m", "This should finish in 5 minutes")
