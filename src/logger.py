from enum import Enum

class Logger:
    class Level(Enum):
        Info = "Info"
        Warning = "Warning"
        Error = "Error"

    def log(self, message: str, level = Level.Info) -> None:
        print(f"[{level.value}]: {message}")
