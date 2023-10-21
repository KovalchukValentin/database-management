from datetime import datetime
from pathlib import Path


class Logger:
   def __init__(self):
       self.format_data = "%d.%m.%Y"
       self.format_time = "%H:%M:%S"
       self.file_path = None
       self.create_today_log_file_if_not_exist()

   def create_today_log_file_if_not_exist(self):
       Path("log").mkdir(parents=True, exist_ok=True)
       self.file_path = Path(f'log/{datetime.now().strftime(self.format_data)}.txt')
       self.file_path.touch(exist_ok=True)

   def add_log(self, log: str):
       current_time = datetime.now().strftime(f"{self.format_data} {self.format_time}")
       with self.file_path.open(mode="a", encoding="utf-8") as file:
           file.write(f"{current_time} {log}\n")


if __name__ == "__main__":
    logger = Logger()
    logger.add_log("Add")
