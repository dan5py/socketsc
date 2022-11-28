import os


__all__ = [
    'Logger',
    'Chalk'
]


class Chalk:
    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    blue = "\033[94m"
    magenta = "\033[95m"
    cyan = "\033[96m"
    white = "\033[97m"
    reset = "\033[0m"

    @staticmethod
    def colorize(text, color):
        return f"{color}{text}{Chalk.reset}"


class Logger:
    @staticmethod
    def log(message):
        print(f"{Chalk.colorize('[LOG]', Chalk.green)} {message}")

    @staticmethod
    def warn(message):
        print(f"{Chalk.colorize('[WARN]', Chalk.yellow)} {message}")

    @staticmethod
    def error(message):
        print(f"{Chalk.colorize('[ERROR]', Chalk.red)} {message}")

    @staticmethod
    def info(message):
        print(f"{Chalk.colorize('[INFO]', Chalk.blue)} {message}")

    @staticmethod
    def debug(message):
        # if os.getenv("DEBUG") == "true":
        if True:
            print(f"{Chalk.colorize('[DEBUG]', Chalk.cyan)} {message}")
