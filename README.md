# Smart File Organizer

A simple desktop app that organizes messy folders by sorting files into folders based on their file type.

Built with **Python** and **Tkinter**. Works on Windows.

## Features

- Select any folder on your computer
- Automatically create category folders: Images, Documents, Videos, Audio, Archives, Programs, Others
- Move files by extension (folders are never moved)
- Safe handling of duplicate names (`file.jpg` → `file_1.jpg`)
- Progress bar and basic statistics
- Dark modern student-project UI

## Requirements

- Python 3.8 or newer
- Tkinter (included with the official Windows Python installer)

No extra packages need to be installed.

## How to Run (Windows)

1. Open **Command Prompt** or **PowerShell**.
2. Go to this project folder:

```bash
cd path\to\desktop_mobile_application
```

3. Run the app:

```bash
python smart_file_organizer.py
```

If `python` does not work, try:

```bash
py smart_file_organizer.py
```

## How to Use

1. Click **Select Folder** and choose the folder you want to clean up.
2. Click **Organize Files**.
3. Wait for the progress bar to finish.
4. Read the success message and statistics.
5. Click **Clear** to reset the screen.

## File Categories

| Folder     | Extensions                                      |
|------------|--------------------------------------------------|
| Images     | jpg, jpeg, png, gif, webp, svg                   |
| Documents  | pdf, doc, docx, txt, xls, xlsx, ppt, pptx         |
| Videos     | mp4, mkv, avi, mov, webm                         |
| Audio      | mp3, wav, ogg, m4a                               |
| Archives   | zip, rar, 7z, tar, gz                            |
| Programs   | exe, msi, bat, py                                |
| Others     | everything else                                  |

## Notes

- Only files in the selected folder are moved (not nested folders).
- Subfolders inside the selected folder are left alone.
- The application file itself is never moved.
- Tip: try it on a test folder first before organizing important files.

## Project Files

```
desktop_mobile_application/
├── smart_file_organizer.py   # Main application
├── requirements.txt          # Dependency notes
└── README.md                 # This file
```
