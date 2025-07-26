import os

def handle_stop_cmd(service_filepath):
    if not os.path.exists(service_filepath):
        # TODO: Print to console saying the service is already started
        return

    os.remove(service_filepath)


