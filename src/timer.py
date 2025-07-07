class Timer:
    def __init__(self, writer):
        self.writer = writer
        self.active = False

    def is_active(self):
        return self.active

    def create(self):
        return True

    def start(self):
        if (self.active):
            return

        self.active = True
        self.writer.write()

    def stop(self):
        self.active = False

