import sys
import json
import os
import time

import psutil

from datetime import datetime, timedelta

from src.start_cmd import handle_start_cmd
from src.stop_cmd import handle_stop_cmd
from src.service_cmd import handle_service_cmd
from src.add_cmd import handle_add_cmd
from src.manage_cmd import handle_manage_cmd
from src.ls_cmd import handle_ls_cmd

timers_filepath = "timers.json"
service_filepath = "kt.pid"

def main():
    # Obtain the args but skip the main executable name
    args = sys.argv[1:]

    if args[0] == "start":
        handle_start_cmd(service_filepath)
    elif args[0] == "stop":
        handle_stop_cmd(service_filepath)
    elif args[0] == "--service":
        handle_service_cmd(timers_filepath, service_filepath)
    elif args[0] == "add":
        handle_add_cmd(timers_filepath, args)
    elif args[0] == "manage":
        handle_manage_cmd(timers_filepath, args)
    elif args[0] == "ls":
        handle_ls_cmd(timers_filepath, args)
    else:
        # TODO: Actually print to shell properly probs using stdout
        print("Not a valid command")
        return

if __name__ == "__main__":
    main()
