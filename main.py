import os
import shutil
import pathlib
from typing import Dict
import pathStorage
import fileProcessing

class Colors:
    """Хранение цветов"""
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


print(os.sep)

def main():
    file_processing = fileProcessing.FileProcessing() # обработчик файлов

    while True:

        command = input("\nВведите команду -> ").split(" ")

        if command[0] == "exit": #чтоб мы могли красиииивооо уйти из программы (отсылка к песне Меладзе)
            break

        # Проверяем, существует ли такая команда
        result = file_processing.router(command[0])
        # Если ДА
        if result:
            try:
                result(*command[1:])
            except TypeError:
                print(f"Команда {command[0]} была вызвана с некорректными аргументами")

        else: #иначе
            commands_str = "\n".join(
                [
                    f"{Colors.OKGREEN}{key}{Colors.ENDC} - {value}"
                    for (key, value) in fileProcessing.FileProcessing.get_commands().items()
                ]
            )
            print(f"Команда {command[0]} не найдена! Список команд:\n{commands_str}")

    print("До новых встреч!")


try:
    if __name__ == "__main__":
        main()
except:
    print("Что-то пошло не так... :(")