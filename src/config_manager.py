from src.writer import IWriter
from src.reader import FileReader

class ConfigManager:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    def generate_timers_file(self, data_generator, file_path = ""):
        self.reader.read()

        if len(self.reader.read_content) == 0:
            data_generator.generate_data()
        else:
            data_generator.generate_data_from_existing(self.reader.read_content)

        self.writer.write_content = data_generator.fetch_data()

        if file_path != "":
            self.writer.path = file_path

        self.writer.write()
        return True
