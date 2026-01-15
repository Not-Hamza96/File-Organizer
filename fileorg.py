import shutil
import os
import time
from concurrent.futures import ThreadPoolExecutor


# A scanner class to Scan and filter files according to category
class FileScanner:
    # constructor to initialize directory
    def __init__(self, directory):
        self.dir = directory

    # function to scan a directory
    def scan_directory(self):
        # listing all files in the given directory
        files = os.listdir(self.dir)
        dir_info = {}
        if not files:
            return {}
        # a dir info dictionary in which the file name is stored as a key and the file path and type is stored as a vale in the form of a tuple
        for file in files:
            path = os.path.join(self.dir, file)
            dir_info[file] = (path, "folder" if os.path.isdir(path) else "file")
        return dir_info

    # a function to get the type of file
    @staticmethod
    def get_cat(file):
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

    # a function to filter the files according to the category
    def filter_files(self, category):
        # a filtered dictionary
        filtered = {}
        # a files dictionary using the scan directory function
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
            # appending the file into the suitable category
            for file in files:
                path = files[file][0]
                # if a file then goes into the type of category else goes into the folders
                if files[file][1] == "file":
                    catg = self.get_cat(file)
                    filtered[catg].append(path)

                else:
                    filtered["Folders"].append(path)
        # to filter based on the size
        elif category == "size":
            filtered = {"small": [], "medium": [], "large": []}
            for file in files:
                path = files[file][0]
                # getting size
                size = os.path.getsize(path)
                # filters based on size 1mb 100mb or large
                if size <= 1024**2:
                    filtered["small"].append(path)
                elif size <= 100 * 1024**2:
                    filtered["medium"].append(path)
                else:
                    filtered["large"].append(path)
        # filtering based on date
        elif category == "date":
            filtered = {"today": [], "yesterday": [], "7d": [], "older": []}
            for file in files:
                path = files[file][0]
                # getting the last modified time
                creation_time = os.path.getmtime(path)
                time_passed = (time.time() - creation_time) // 86400
                # converting time into days
                if time_passed < 1:
                    filtered["today"].append(path)
                elif time_passed < 2:
                    filtered["yesterday"].append(path)
                elif time_passed < 7:
                    filtered["7d"].append(path)
                else:
                    filtered["older"].append(path)
        return filtered


# a file moving class
class FileMover:
    # initializing filtered data and base path and the moving data of a file
    def __init__(self, filtered_data, base):
        self.data = filtered_data
        self.base = base
        self.moves = []

    # a mover function to move a file from its original path to a folder
    def mover(self, path, folder):
        try:
            shutil.move(path, os.path.join(self.base, folder))
        except FileExistsError:
            print(f"Destination path {folder} already exists")

    # a folder creator for the filtered data
    def folder_creator(self):
        for cat, path in self.data.items():
            if not path:
                continue
            folder_path = os.path.join(self.base, cat)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    # a dry run function to give a glance before the original moving happens
    def dry_runner(self):
        for cat, paths in self.data.items():
            if not paths:
                continue
            for path in paths:
                print(f"Moving {os.path.basename(path)} to {cat} Folder")

    # a file mover function to move files by accessing their path from the filtered data using threadpoolexecuter
    def file_mover(self):
        # creating folders
        self.folder_creator()
        with ThreadPoolExecutor() as exe:
            processes = []
            for cat, paths in self.data.items():
                if not paths:
                    continue
                for path in paths:
                    result = exe.submit(self.mover, path, cat)
                    processes.append(result)
                    # appending the file moves into the self.moves list in the form of a tuple with the file name and folder path
                    self.moves.append(
                        (os.path.basename(path), os.path.join(self.base, cat))
                    )

                print(f"{len(self.data[cat])} Files moved to {cat} Folder")
        print("Operation Completed✅")

    # an undo function for the recently moved files
    def Undo(self):

        with ThreadPoolExecutor() as e:

            for paths in self.moves:
                # accessing the self.moves to undo the movement
                file_path = os.path.join(paths[1], paths[0])
                res = e.submit(self.mover, file_path, self.base)

        # deleting the folders created

        with ThreadPoolExecutor() as e:
            for paths in self.moves:
                if os.path.exists(paths[1]):
                    res = e.submit(shutil.rmtree, paths[1], ignore_errors=True)

            print("Operation Completed✅ . Files Moved To Their Original Path")


# a main engine class to handle user input
class MainEngine:
    # a worker method to make an instance of the classes
    def worker(self, typ, path):
        # making an instance of the scanner class and passing in the path
        scanner = FileScanner(path)
        # getting the filtered data
        data = scanner.filter_files(typ)
        # making an instance of the filemover class
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

    # a main method to handle user input
    def main(self):

        while True:
            print("-" * 32)
            print("File Organizer".center(32))
            print("-" * 32)
            path = input("Enter The Path of the folder or disk to organize: ")
            if os.path.exists(rf"{path}"):
                try:
                    ch = int(
                        input("1. Sort By Type\n2. Sort By Size\n3. Sort By Time: ")
                    )
                    if ch == 1:
                        self.worker("type", path)
                    elif ch == 2:
                        self.worker("size", path)
                    elif ch == 3:
                        self.worker("date", path)
                    else:
                        print("Invalid Choice")
                except ValueError:
                    print("Please Enter a number")
            else:
                print("Path Does not Exist")


system = MainEngine()
system.main()
