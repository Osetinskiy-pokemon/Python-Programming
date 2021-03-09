import os
import shutil
import pathlib
from typing import Dict

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


class PathStorage:
    """Здесь ведется работа с путями (хранится информация)"""

    def __init__(self) -> None:
        self.__storage = ["storage"]

    def add_path(self, path: str) -> None:
        """Добавляет файл в иерархию каталогов"""
        # Если хотим выйти на уровень выше
        if ".." in path and len(self.__storage) != 1:
            self.__storage.pop(-1)
        # Если хотим выйти за пределы Вселенной
        elif ".." in path:
            print("Вы хотите выйти за пределы этой Вселенной!")
        # Значит хотим перейти на уровень ниже
        else:
            self.__storage.append(path)

    def file2path(self, file_name: str) -> str:
        """Возвращает указанный файл в текущей иерархии каталогов"""
        locale_storage = self.__storage.copy()
        locale_storage.append(file_name)
        abs_path = pathlib.Path(__file__).parent.absolute()
        return str(abs_path) + "/" + "/".join(locale_storage)

    @property
    def path(self):
        """Возвращает текущую иерархию каталогов"""
        abs_path = pathlib.Path(__file__).parent.absolute()
        return str(abs_path) + "/" + "/".join(self.__storage)

    @property
    def upper_path(self):
        """Возвращает директорию выше текущей"""
        abs_path = pathlib.Path(__file__).parent.absolute()
        print(self.__storage[1:])
        return str(abs_path) + "/" + "/".join(self.__storage[:1])
