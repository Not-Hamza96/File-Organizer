import shutil
import os
import time
from concurrent.futures import ThreadPoolExecutor


class FileScanner:
    def __init__(self, directory):
        self.dir = directory

    def scan_directory(self):
        files = os.listdir(self.dir)
        dir_info = {}
        if not files:
            return {}
        for file in files:
            path = os.path.join(self.dir, file)
            dir_info[file] = (path, "folder" if os.path.isdir(path) else "file")
        return dir_info

    def get_cat(self, file):
        category = {
            "Images": (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"),
            "Documents": (".pdf", ".docx", ".xlsx", ".txt", ".csv", ".pptx"),
            "Videos": (".mp4", ".mov", ".avi", ".mkv", ".wmv"),
            "Audios": (".wav", ".mp3", ".aac"),
            "Programs": (".py", ".java", ".cs", ".js", ".php", ".sql", ".html"),
            "Exe": (".exe"),
        }
        for cat, extension in category.items():
            if file.lower().endswith(extension):
                return cat
        return "Misc"

    def filter_files(self, category):
        filtered = {}
        files = self.scan_directory()
        if not files:
            return {}
        if category == "type":

            filtered = {
                "Images": [],
                "Documents": [],
                "Audios": [],
                "Videos": [],
                "Folders": [],
                "Programs": [],
                "Exe": [],
                "Misc": [],
            }
            for file in files:
                path = files[file][0]
                if files[file][1] == "file":
                    catg = self.get_cat(file)
                    filtered[catg].append(path)

                else:
                    filtered["Folders"].append(path)
        elif category == "size":
            filtered = {"small": [], "medium": [], "large": []}
            for file in files:
                path = files[file][0]
                size = os.path.getsize(path)

                if size <= 1024**2:
                    filtered["small"].append(path)
                elif size <= 100 * 1024**2:
                    filtered["medium"].append(path)
                else:
                    filtered["large"].append(path)

        elif category == "date":
            filtered = {"today": [], "yesterday": [], "7d": [], "older": []}
            for file in files:
                path = files[file][0]
                creation_time = os.path.getmtime(path)
                time_passed = (time.time() - creation_time) // 86400
                if time_passed < 1:
                    filtered["today"].append(path)
                elif time_passed < 2:
                    filtered["yesterday"].append(path)
                elif time_passed < 7:
                    filtered["7d"].append(path)
                else:
                    filtered["Older"].append(path)
        return filtered


class FileMover:
    def __init__(self, filtered_data, base):
        self.data = filtered_data
        self.base = base
        self.moves = []

    def mover(self, path, folder):
        try:
            shutil.move(path, os.path.join(self.base, folder))
        except FileExistsError:
            print(f"Destination path {folder} already exists")

    def folder_creator(self):
        for cat, path in self.data.items():
            if not path:
                continue
            folder_path = os.path.join(self.base, cat)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def dry_runner(self):
        for cat, paths in self.data.items():
            if not paths:
                continue
            for path in paths:
                print(f"Moving {os.path.basename(path)} to {cat} Folder")

    def file_mover(self):
        self.folder_creator()
        for cat, paths in self.data.items():
            if not paths:
                continue
            for path in paths:
                self.mover(path, cat)
                self.moves.append(
                    (os.path.basename(path), os.path.join(self.base, cat))
                )

    def Undo(self):
        for paths in self.moves:
            file_path = os.path.join(paths[1], paths[0])
            self.mover(file_path, self.base)
        for paths in self.moves:
            if os.path.exists(paths[1]):
                shutil.rmtree(paths[1], ignore_errors=True)


class MainEngine:
    def worker(self, typ, path):
        scanner = FileScanner(path)
        data = scanner.filter_files(typ)
        mover = FileMover(data, path)
        dry_run = input("Dry Run Before Moving(y/n): ")
        if dry_run.lower() == "y":
            mover.dry_runner()
            ch = input("Continue (y/n): ").lower()
            if ch != "y":
                return
            mover.file_mover()
        else:
            mover.file_mover()
            ch = input("Undo? OR Continue?(u/c)")
            if ch.lower() == "u":
                mover.Undo()
            else:
                return

    def main(self):
        print("-" * 32)
        print("File Organizer".center(32))
        print("-" * 32)
        while True:
            path = input("Enter The Path of the folder or disk to organize: ")
            if os.path.exists(rf"{path}"):
                ch = int(input("1. Sort By Type\n2. Sort By Size\n3. Sort By Time: "))
                if ch == 1:
                    self.worker("type", path)
                elif ch == 2:
                    self.worker("size", path)
                elif ch == 3:
                    self.worker("date", path)
                else:
                    print("Invalid Choice")
            else:
                print("Path Does not Exist")


system = MainEngine()
system.main()
