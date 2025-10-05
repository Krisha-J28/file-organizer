import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import shutil
import os
from datetime import datetime

# vars for storing selected paths
source_folder_path = ""
destination_folder = ""
report_file_path = ""

file_type = {  
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".csv", ".ppt", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".ico", ".heic", ".raw"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm", ".mpeg", ".3gp", ".m4v"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma", ".aiff"],
    "Code": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css", ".php", ".rb", ".swift", ".ts", ".sql"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"],
    "Executables": [".exe", ".msi", ".bat", ".sh", ".apk", ".bin", ".jar"],
    "Spreadsheets": [".xls", ".xlsx", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    "System": [".dll", ".sys", ".ini", ".dat", ".tmp", ".log"],
    "Database": [".db", ".sqlite", ".sql", ".mdb", ".accdb"]
}

def sort(file_extension):
    for category, extensions in file_type.items():
        if file_extension in extensions:
            return category
    return "Others"

def organize_files():
    
    global source_folder_path, destination_folder, report_file_path

    print("\n=== Basic file organization script ===")

    if not source_folder_path:
        print("Source folder not selected. Please select it again.")
        return

    if not destination_folder:
        print("Destination folder not selected. Please select it again.")
        return

    source_dir = Path(source_folder_path)
    destination_dir = Path(destination_folder)

    if not source_dir.exists():
        print(f"\nSource directory '{source_dir}' does not exist.")
        return

    if not destination_dir.exists():
        print(f"Destination directory '{destination_dir}' does not exist. Creating it!")
        try:
            destination_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Error creating destination directory: {e}")
            return

    report_file_path = os.path.join(destination_folder, "log.txt") #for storing report file in destination folder itself.

    print(f"\nOrganizing files from {source_dir} to {destination_dir} ...\n")
    files_moved = 0

    try:
        all_files = [f for f in source_dir.rglob("*") if f.is_file()]
        total_files = len(all_files)
        progress["maximum"] = total_files

        with open(report_file_path, "w") as report_file:
            # for item_path in source_dir.rglob("*"):
            #     if item_path.is_file():
             for idx, item_path in enumerate(all_files, 1):
                    file_extension = item_path.suffix.lower()
                    if not file_extension:
                        print(f"Skipping {item_path} as it has no extension.")
                        continue

                    print(f"\nProcessing file: {item_path.name} with extension {file_extension}")

                    dest_folder_name = sort(file_extension)
                    if not dest_folder_name:
                        print(f"Skipping {item_path} as it has no valid extension.")
                        continue

                    category_folder = destination_dir / dest_folder_name

                    try:
                        category_folder.mkdir(parents=True, exist_ok=True)
                    except Exception as e:
                        print(f"Error creating category folder : {e}")
                        continue

                    destination_file_path = category_folder / item_path.name # here path (+)& string = path

                    try:
                        shutil.move(str(item_path), str(destination_file_path)) # moves here
                        print(f"Moved {item_path.name} to {category_folder}\n")
                        timestamp = datetime.now().strftime('%a, %Y-%m-%d %H:%M:%S') # A for day's full name.
                        report_file.write(f"Moved: {item_path.name} -> {category_folder}  :: {timestamp}\n") # report content
                        # report_file.write(f"Moved: {item_path.name} -> {category_folder}  :: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        files_moved += 1
                        progress["value"] = idx #progress bar
                        root.update_idletasks()  #progress bar
                    except Exception as e:
                        print(f"Error moving file: {item_path.name}: {e}")
                        report_file.write(f"ERROR moving {item_path.name}: {e}\n")

        print(f"\n\nFile organization complete. {files_moved} files moved.")
        print("\nReport saved at:", report_file_path)

    except Exception as e:
        print(f"Unexpected error during organization: {e}") # incase of ANY error in general. (while organising) 

# UDFs we'll directly call on respective button's click
def open_source_folder_dialog():
    global source_folder_path
    folder_selected = filedialog.askdirectory(title="Select Folder to Organise")   # title
    if folder_selected:
        source_folder_path = folder_selected
        source_label.config(text=f"Source: {source_folder_path}")    # a label inside GUI shows path to cross-verify.

def open_destination_folder_dialog():
    global destination_folder, report_file_path
    destination_folder = filedialog.askdirectory(title="Select Destination Folder")
    if destination_folder:
        # destination_folder = folder_selected
        report_file_path = os.path.join(destination_folder, "log.txt")
        destination_label.config(text=f"Destination: {destination_folder}")
# to open organised folder & report
def open_destination_folder():
    if os.path.exists(destination_folder):
        os.startfile(destination_folder)
    else:
        status_label.config(text="Organized folder not found!") # incase of error

def open_report():
    if os.path.exists(report_file_path):
        os.startfile(report_file_path)
    else:
        status_label.config(text="Report file not found!")

# Main window
root = tk.Tk()
root.title("File Organizer")
root.geometry("800x510")
root.configure(bg="#f0f4f7")  # light blueish background
root.resizable(True, True)

style = ttk.Style()
style.theme_use('default')
style.configure("green.Horizontal.TProgressbar", 
                troughcolor="#e0e0e0", 
                background="#28a745", 
                thickness=20)

# Heading
heading = tk.Label(root, text="Organize Your Files", font=("Helvetica", 20, "bold"), bg="#f0f4f7", fg="#003366")
heading.pack(pady=20)

# Frame for buttons
button_frame = tk.Frame(root, bg="#f0f4f7")
button_frame.pack(pady=10)

btn1 = tk.Button(button_frame, text="Select Source Folder", command=open_source_folder_dialog,
                 font=("Segoe UI", 12), bg="#007acc", fg="white", padx=10, pady=5)
btn1.pack(pady=10, fill="x")

btn2 = tk.Button(button_frame, text="Select Destination Folder", command=open_destination_folder_dialog,
                 font=("Segoe UI", 12), bg="#007acc", fg="white", padx=10, pady=5)
btn2.pack(pady=10, fill="x")

btn3 = tk.Button(button_frame, text="Start Organizing Files", command=organize_files,
                 font=("Segoe UI", 12, "bold"), bg="#28a745", fg="white", padx=10, pady=5)
btn3.pack(pady=15, fill="x")

btn4 = tk.Button(button_frame, text="Open Organized Folder", command=open_destination_folder,
                 font=("Segoe UI", 11), bg="#17a2b8", fg="white", padx=10, pady=5)
btn4.pack(pady=5, fill="x")

btn5 = tk.Button(button_frame, text="📄 Open Report File", command=open_report,
                 font=("Segoe UI", 11), bg="#6f42c1", fg="white", padx=10, pady=5)
btn5.pack(pady=5, fill="x")

# Labels to show selected folders
label_frame = tk.Frame(root, bg="#f0f4f7")
label_frame.pack(pady=10)

source_label = tk.Label(label_frame, text="Source: Not selected", bg="#f0f4f7", fg="#333", font=("Calibri", 11))
source_label.pack(pady=3)

destination_label = tk.Label(label_frame, text="Destination: Not selected", bg="#f0f4f7", fg="#333", font=("Calibri", 11))
destination_label.pack(pady=3)

# progress bar
progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate", style="green.Horizontal.TProgressbar")
progress.pack(pady=5)

# Status label at bottom
status_label = tk.Label(root, text="", font=("Calibri", 11, "italic"), fg="red", bg="#f0f4f7")
status_label.pack(pady=10)

# Run the application
root.mainloop()