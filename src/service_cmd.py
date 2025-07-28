import os
import time
import json

from datetime import datetime, timedelta

from winotify import Notification, audio

def handle_service_cmd(timers_filepath, service_filepath):
    with open(service_filepath, "w") as file_handle:
        file_handle.write(str(os.getpid()))

    while True:
        time.sleep(1)

        if not os.path.exists(service_filepath):
            break

        read_content = None

        try:
            with open(timers_filepath, "r") as file_handle:
                read_content = file_handle.read()
        except Exception as e:
            # TODO: Actually print to shell properly probs using stdout
            print(f"Exception: {e}")

        json_obj = json.loads(read_content)

        current_time = datetime.now()

        for idx, item in enumerate(json_obj):
            timestamp = datetime.fromisoformat(item["timestamp"])

            if item.get("pause-timestamp"):
                current_time = datetime.fromisoformat(item["pause-timestamp"])

            if (current_time >= timestamp):
                try:
                    with open(timers_filepath, "w") as file_handle:
                        json_obj.pop(idx)
                        json.dump(json_obj, file_handle, indent=2)

                        toast = Notification(app_id="k timer (kt)",
                                             title=item["message"],
                                             #msg="test"
                                             duration="long" if current_time >= timestamp else "short") # Missed notifications will appear for a shorter amount of time

                        toast.set_audio(audio.LoopingAlarm9, loop=True)
                        toast.add_actions(label="Dismiss")
                        toast.show()

                except Exception as e:
                    # TODO: Actually print to shell properly probs using stdout
                    print(f"Exception: {e}")

        # JSON object no longer has items
        if not json_obj:
            break

