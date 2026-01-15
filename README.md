📂 File Organizer (Python)

A command-line based File Organizer written in Python that automatically organizes files in a directory based on type, size, or date, with support for dry runs, undo operations, and multithreaded file moving.
This project is designed to safely clean up messy folders while giving the user full control over the process.

🚀 Features
📁 Sort files by type
Images, Documents, Videos, Audios, Programs, Executables, Misc

📏 Sort files by size
Small (≤ 1 MB)
Medium (≤ 100 MB)
Large (> 100 MB)

🕒 Sort files by date
Today
Yesterday
Last 7 Days
Older

👀 Dry Run mode
Preview file movements before executing them

↩️ Undo functionality
Revert all file movements made in the last operation

⚡ Multithreaded file operations
Faster file movement using ThreadPoolExecutor

🧠 Extensible design
Easily add new file categories or rules

🛠️ Technologies Used
Python 3
os – directory and file handling
shutil – file movement
time – date-based filtering
concurrent.futures.ThreadPoolExecutor – multithreading

📁 File Categorization Rules
Category	      Extensions
Images	      .png, .jpg, .jpeg, .webp, .bmp, .gif
Documents	    .pdf, .docx, .xlsx, .txt, .csv, .pptx
Videos	      .mp4, .mov, .avi, .mkv, .wmv
Audios	      .wav, .mp3, .aac
Programs	    .py, .java, .cs, .js, .php, .sql, .html
Executables	  .exe
Misc	        Any unsupported file type
▶️ How to Run

Clone the repository
git clone https://github.com/your-username/file-organizer.git
cd file-organizer

Run the script
python fileorg.py


Follow the on-screen prompts
Enter the folder or disk path
Choose sorting method
Preview with Dry Run (optional)
Confirm file movement
Undo if needed

📌 Example Workflow
Enter The Path of the folder or disk to organize: D:\Downloads
1. Sort By Type
2. Sort By Size
3. Sort By Time

Dry Run Before Moving (y/n): y
Moving image1.png to Images Folder
Moving report.pdf to Documents Folder
Continue (y/n): y
Operation Completed ✅
Undo? OR Continue? (u/c)

⚠️ Notes & Limitations

Works on top-level files only (no recursive folder scanning yet)
Files currently open or locked by another program may fail to move
Designed for local file systems
Tested primarily on Windows


📜 License
This project is open-source and free to use for learning and personal projects.

👨‍💻 Author

Hamza
Student | Python Developer | Aspiring Software Engineer

