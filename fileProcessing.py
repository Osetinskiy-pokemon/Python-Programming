import os
import shutil
import pathlib
from typing import Dict
import pathStorage

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


class FileProcessing:
    """Тут происходит работа, связанная с файлами"""

    @staticmethod
    def get_commands() -> Dict[str, str]:
        """Выводится список возможных команд"""

        commands_dict = {
            "travel": "Перемещение между папками",
            "content": "Вывод содержимого текущей папки на экран",
            "mkfold": "Создание папки",
            "rmfold": "Удаление папки",
            "create": "Создание файла",
            "new_name": "Переименование файла/папки",
            "reading": "Чтение файла",
            "destroy": "Удаление файла",
            "replicate": "Копирование файла/папки",
            "moving": "Перемещение файла/папки",
            "compose": "Запись в файл",
        }

        return commands_dict

    def __init__(self) -> None:
        self.storage = pathStorage.PathStorage()

    def mkfold(self, filename: str):
        """Создание папки (с указанием имени)"""
        current_path = self.storage.file2path(filename)
        try:
            os.mkdir(current_path)
        except FileNotFoundError:
            os.makedirs(current_path)
        except FileExistsError:
            print(f"Директория {filename} уже существует")

    def rmfold(self, filename: str):
        """Удаление папки по имени"""
        current_path = self.storage.file2path(filename)
        try:
            os.rmdir(current_path)
        except OSError:
            try:
                shutil.rmtree(current_path, ignore_errors=False, onerror=None)
            except FileNotFoundError:
                print(f"Директория {filename} не найдена")
            except NotADirectoryError:
                print(f"Файл {filename} не является директорией")
        except FileNotFoundError:
            print(f"Директория {filename} не найдена")
        except NotADirectoryError:
            print(f"Файл {filename} не является директорией")

    def travel(self, filename: str):
        """
        Перемещение между папками может осуществляться на уровень выше, заходя по имени папки
        и в пределах текущей директории
        """
        self.storage.add_path(filename)
        current_path = self.storage.path

        try:
            os.chdir(current_path)
        except FileNotFoundError:
            self.storage.add_path("../")
            print(f"Директория {filename} не найдена")
        except NotADirectoryError:
            self.storage.add_path("../")
            print(f"Файл {filename} не является директорией")

    def content(self):
        """
        Показать содержимое папки
        """
        current_path = self.storage.path
        filelist = os.listdir(current_path)
        for i in range(len(filelist)):
            if os.path.isdir(self.storage.file2path(filelist[i])):
                filelist[i] = f"[dir] {Colors.OKCYAN}{filelist[i]}{Colors.ENDC}"
            elif os.path.isfile(self.storage.file2path(filelist[i])):
                filelist[i] = f"[file] {Colors.WARNING}{filelist[i]}{Colors.ENDC}"

        r = "\n".join(filelist)
        print(f"Содержимое {current_path}:\n{r}")

    def touch(self, filename: str):
        """Создание новых файлов, в качестве параметра - имя файла"""
        current_path = self.storage.file2path(filename)
        try:
            open(current_path, "a").close()
        except IsADirectoryError:
            print(f"Директория с именем {filename} уже существует. Придумайте другое название")

    def cat(self, filename: str) -> str:
        """Чтение файла"""
        current_path = self.storage.file2path(filename)
        try:
            with open(current_path, "r") as file:
                print(file.read())
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
        except IsADirectoryError:
            print(f"Файл {filename} является директорией")

    def new_name(self, filename_old: str, filename_new: str):
        """Переименование файла"""

        path_old = self.storage.file2path(filename_old)
        path_new = self.storage.file2path(filename_new)

        # На случай, если файл с именем уже существует
        try:
            if not os.path.isfile(path_new):
                os.rename(path_old, path_new)
            else:
                raise IsADirectoryError
        except FileNotFoundError:
            print(f"Указанного файла {filename_old} не существует")
        except IsADirectoryError:
            print(f"Файл с названием {filename_new} уже существует")

    def rm(self, filename: str):
        """Удаление, в качестве параметра - имя файла"""
        path = self.storage.file2path(filename)
        if os.path.isfile(path):
            os.remove(path)
        else:
            print(f"Файла {filename} не существует")

    def cp(self, filename: str, path: str):
        """Копирование файла из одной папки в другую"""
        path_old = self.storage.file2path(filename)
        # Копирование на уровень выше
        if ".." in path:
            path_new = self.storage.upper_path + "/" + filename
        else:
            # Проверяем на то, что это за тип файла
            buff = self.storage.file2path(path)

            # Если конечный путь папка - закидываем туда файл
            if os.path.isdir(buff):
                path_new = self.storage.file2path(path + "/" + filename)
            else:
                # Значит это копирование на одном уровне
                path_new = self.storage.file2path(path)
        try:
            shutil.copyfile(path_old, path_new)
        # Если это директория - копируем директорию
        except IsADirectoryError:
            shutil.copytree(path_old, path_new)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    def mv(self, filename: str, path: str):
        """Перемещение файла"""
        path_old = self.storage.file2path(filename)
        if ".." in path:
            path_new = self.storage.upper_path + "/" + filename
        else:
            # Проверяем на то, что это за тип файла
            buff = self.storage.file2path(path)
            # Если директория - закидываем туда файл
            if os.path.isdir(buff):
                path_new = self.storage.file2path(path + "/" + filename)
            else:
                # Значит это перемещение на одном уровне
                path_new = self.storage.file2path(path)
        try:
            shutil.move(path_old, path_new)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    def write(self, filename: str, *data: str):
        """Запись в файл"""
        text = " ".join(data)
        path = self.storage.file2path(filename)
        try:
            with open(path, "a") as file:
                file.write(text)
        except IsADirectoryError:
            print(f"Указанный файл {filename} - директория")

    def router(self, command: str):
        """Параллель между командами и методами FileProcessing"""

        commands = [
            self.travel,
            self.content,
            self.mkfold,
            self.rmfold,
            self.touch,
            self.new_name,
            self.cat,
            self.rm,
            self.cp,
            self.mv,
            self.write,
        ]
        item_dict = dict(zip(FileProcessing.get_commands().keys(), commands))
        return item_dict.get(command, None)