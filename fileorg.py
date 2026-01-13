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
                    if file.lower().endswith(
                        (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif")
                    ):
                        filtered["Images"].append(path)
                    elif file.lower().endswith(
                        (".pdf", ".docx", ".xlsx", ".txt", ".csv", ".pptx")
                    ):
                        filtered["Documents"].append(path)
                    elif file.lower().endswith(
                        (".mp4", ".mov", ".avi", ".mkv", ".wmv")
                    ):
                        filtered["Videos"].append(path)
                    elif file.lower().endswith((".wav", ".mp3", ".aac")):
                        filtered["Audios"].append(path)
                    elif file.lower().endswith(
                        (".py", ".java", ".cs", ".js", ".php", ".sql", ".html")
                    ):
                        filtered["Programs"].append(path)
                    elif file.lower().endswith(".exe"):
                        filtered["Exe"].append(path)
                    else:
                        filtered["Misc"].append(path)

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
            filtered = {"today": [], "yesterday": [], "7d": [], "Older": []}
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
        self.dry_run = False
        self.moves = []

    def mover(self, path, folder):
        try:
            shutil.move(path, os.path.join(self.base, folder))
        except FileExistsError:
            print("Destination path already exists")

    def folder_creator(self):
        for cat, path in self.data.items():
            if not path:
                continue
            if not os.path.exists(cat):
                os.makedirs(os.path.join(self.base, cat), exist_ok=True)

    def file_mover(self):

        ch = input("Dry Run Before Organizing?(y/n)")
        if ch.lower() == "y":
            self.dry_run = True
        if self.dry_run == True:
            for cat, paths in self.data.items():
                if not paths:
                    continue
                for path in paths:
                    print(f"Moving {os.path.basename(path)} to {cat}...")
            c = input("Continue OR Exit?(c/e)")
            if c.lower() == "c":
                self.dry_run = False
        if self.dry_run == False:
            self.folder_creator()
            for cat, paths in self.data.items():
                if not paths:
                    continue
                for path in paths:
                    self.mover(path, cat)
                    self.moves.append((path, os.path.join(self.base, cat)))

    def Undo(self):
        for paths in self.moves:
            files = os.listdir(paths[1])
            for file in files:
                path = os.path.join(paths[1], file)
                self.mover(path, self.base)
        for paths in self.moves:
            if os.path.exists(paths[1]):
                shutil.rmtree(paths[1])


class MainEngine:
    def worker(self, typ, path):
        scanner = FileScanner(path)
        data = scanner.filter_files(typ)
        mover = FileMover(data, path)
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
                ch = int(input("1. Sort By Type\n2. Sort By Size\n3. Sort By Time"))
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
