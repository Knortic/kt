from src.writer import IWriter

class ConfigManager:
    def __init__(self, writer):
        self.writer = writer

    def generate_timers_file(self, file_path):
        self.writer.write_content = "test"
        self.writer.path = file_path
        self.writer.write()
        return True
