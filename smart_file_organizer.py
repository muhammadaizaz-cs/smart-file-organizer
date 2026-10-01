"""
Smart File Organizer
A simple desktop app that sorts files into folders by file type.
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path


# File type categories and their extensions
CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
    "Audio": {".mp3", ".wav", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Programs": {".exe", ".msi", ".bat", ".py"},
}

CATEGORY_NAMES = list(CATEGORIES.keys()) + ["Others"]


def get_category(extension: str) -> str:
    """Return the folder name for a given file extension."""
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def unique_destination(dest_folder: Path, filename: str) -> Path:
    """
    Return a path that does not already exist.
    If file.jpg exists, try file_1.jpg, file_2.jpg, and so on.
    """
    destination = dest_folder / filename
    if not destination.exists():
        return destination

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        destination = dest_folder / new_name
        if not destination.exists():
            return destination
        counter += 1


class SmartFileOrganizer(tk.Tk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.title("Smart File Organizer")
        self.geometry("560x520")
        self.minsize(480, 480)
        self.resizable(True, True)

        # Path of this script — never move ourselves
        self.app_path = Path(__file__).resolve()
        self.selected_folder = tk.StringVar(value="No folder selected")

        self._setup_theme()
        self._build_ui()

    def _setup_theme(self):
        """Apply a simple dark modern theme."""
        self.colors = {
            "bg": "#1e1e2e",
            "surface": "#2a2a3d",
            "accent": "#4a9eff",
            "accent_hover": "#3a8eef",
            "text": "#e8e8f0",
            "text_dim": "#a0a0b8",
            "success": "#4ade80",
            "border": "#3a3a50",
        }

        self.configure(bg=self.colors["bg"])

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "TProgressbar",
            troughcolor=self.colors["surface"],
            background=self.colors["accent"],
            bordercolor=self.colors["border"],
            lightcolor=self.colors["accent"],
            darkcolor=self.colors["accent"],
            thickness=16,
        )

    def _build_ui(self):
        """Create all widgets."""
        pad = {"padx": 24, "pady": 8}

        # Title
        title = tk.Label(
            self,
            text="Smart File Organizer",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
        )
        title.pack(pady=(28, 4))

        subtitle = tk.Label(
            self,
            text="Sort messy folders by file type automatically",
            font=("Segoe UI", 10),
            bg=self.colors["bg"],
            fg=self.colors["text_dim"],
        )
        subtitle.pack(pady=(0, 16))

        # Folder selection row
        folder_frame = tk.Frame(self, bg=self.colors["bg"])
        folder_frame.pack(fill="x", **pad)

        self.folder_label = tk.Label(
            folder_frame,
            textvariable=self.selected_folder,
            font=("Segoe UI", 9),
            bg=self.colors["surface"],
            fg=self.colors["text_dim"],
            anchor="w",
            padx=12,
            pady=10,
            relief="flat",
        )
        self.folder_label.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.select_btn = self._make_button(
            folder_frame, "Select Folder", self.select_folder, width=14
        )
        self.select_btn.pack(side="right")

        # Action buttons
        btn_frame = tk.Frame(self, bg=self.colors["bg"])
        btn_frame.pack(pady=12)

        self.organize_btn = self._make_button(
            btn_frame, "Organize Files", self.organize_files, width=16, primary=True
        )
        self.organize_btn.pack(side="left", padx=6)

        self.clear_btn = self._make_button(
            btn_frame, "Clear", self.clear_all, width=10
        )
        self.clear_btn.pack(side="left", padx=6)

        # Progress bar
        progress_frame = tk.Frame(self, bg=self.colors["bg"])
        progress_frame.pack(fill="x", padx=24, pady=(8, 4))

        self.progress = ttk.Progressbar(
            progress_frame, mode="determinate", maximum=100, value=0
        )
        self.progress.pack(fill="x")

        self.status_label = tk.Label(
            self,
            text="Ready",
            font=("Segoe UI", 9),
            bg=self.colors["bg"],
            fg=self.colors["text_dim"],
        )
        self.status_label.pack(pady=(4, 12))

        # Statistics panel
        stats_outer = tk.Frame(self, bg=self.colors["surface"], padx=20, pady=16)
        stats_outer.pack(fill="x", padx=24, pady=8)

        stats_title = tk.Label(
            stats_outer,
            text="Statistics",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["surface"],
            fg=self.colors["text"],
        )
        stats_title.pack(anchor="w", pady=(0, 10))

        self.stat_total = self._make_stat_row(stats_outer, "Total Files:")
        self.stat_organized = self._make_stat_row(stats_outer, "Organized Files:")
        self.stat_skipped = self._make_stat_row(stats_outer, "Skipped Files:")

        # Footer
        footer = tk.Label(
            self,
            text="Folders are never moved  ·  Duplicate names are renamed safely",
            font=("Segoe UI", 8),
            bg=self.colors["bg"],
            fg=self.colors["text_dim"],
        )
        footer.pack(side="bottom", pady=16)

    def _make_button(self, parent, text, command, width=12, primary=False):
        """Create a styled button."""
        bg = self.colors["accent"] if primary else self.colors["surface"]
        fg = "#ffffff" if primary else self.colors["text"]
        active_bg = self.colors["accent_hover"] if primary else self.colors["border"]

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10),
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=fg,
            relief="flat",
            width=width,
            cursor="hand2",
            padx=8,
            pady=6,
        )
        return btn

    def _make_stat_row(self, parent, label_text):
        """Create a label + value row for statistics."""
        row = tk.Frame(parent, bg=self.colors["surface"])
        row.pack(fill="x", pady=3)

        label = tk.Label(
            row,
            text=label_text,
            font=("Segoe UI", 10),
            bg=self.colors["surface"],
            fg=self.colors["text_dim"],
            width=16,
            anchor="w",
        )
        label.pack(side="left")

        value = tk.Label(
            row,
            text="0",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["surface"],
            fg=self.colors["text"],
            anchor="w",
        )
        value.pack(side="left")
        return value

    def select_folder(self):
        """Open a dialog for the user to pick a folder."""
        try:
            folder = filedialog.askdirectory(title="Select a folder to organize")
            if folder:
                self.selected_folder.set(folder)
                self.status_label.config(
                    text="Folder selected. Click Organize Files.",
                    fg=self.colors["text_dim"],
                )
                self._reset_stats()
                self.progress["value"] = 0
        except Exception as exc:
            messagebox.showerror("Error", f"Could not select folder:\n{exc}")

    def clear_all(self):
        """Reset the UI to its initial state."""
        self.selected_folder.set("No folder selected")
        self.status_label.config(text="Ready", fg=self.colors["text_dim"])
        self.progress["value"] = 0
        self._reset_stats()

    def _reset_stats(self):
        self.stat_total.config(text="0")
        self.stat_organized.config(text="0")
        self.stat_skipped.config(text="0")

    def organize_files(self):
        """Scan the selected folder and move files into category folders."""
        folder_path = self.selected_folder.get()

        if not folder_path or folder_path == "No folder selected":
            messagebox.showwarning("No Folder", "Please select a folder first.")
            return

        folder = Path(folder_path)

        if not folder.is_dir():
            messagebox.showerror("Invalid Folder", "The selected path is not a valid folder.")
            return

        try:
            # Collect only files in the top level (do not move folders)
            files = [
                item
                for item in folder.iterdir()
                if item.is_file() and item.resolve() != self.app_path
            ]
        except PermissionError:
            messagebox.showerror("Permission Denied", "Cannot read the selected folder.")
            return
        except Exception as exc:
            messagebox.showerror("Error", f"Could not read folder:\n{exc}")
            return

        total = len(files)
        if total == 0:
            messagebox.showinfo("Nothing to Organize", "No files found in this folder.")
            self.stat_total.config(text="0")
            self.stat_organized.config(text="0")
            self.stat_skipped.config(text="0")
            return

        # Create category folders if they do not exist
        try:
            for name in CATEGORY_NAMES:
                (folder / name).mkdir(exist_ok=True)
        except Exception as exc:
            messagebox.showerror("Error", f"Could not create folders:\n{exc}")
            return

        organized = 0
        skipped = 0
        self.progress["value"] = 0
        self.progress["maximum"] = total
        self.status_label.config(text="Organizing...")
        self.organize_btn.config(state="disabled")
        self.select_btn.config(state="disabled")
        self.clear_btn.config(state="disabled")
        self.update_idletasks()

        try:
            for index, file_path in enumerate(files, start=1):
                try:
                    category = get_category(file_path.suffix)
                    dest_folder = folder / category
                    destination = unique_destination(dest_folder, file_path.name)

                    # Skip if somehow source and destination are the same
                    if file_path.resolve() == destination.resolve():
                        skipped += 1
                    else:
                        shutil.move(str(file_path), str(destination))
                        organized += 1
                except Exception:
                    skipped += 1

                self.progress["value"] = index
                self.stat_total.config(text=str(total))
                self.stat_organized.config(text=str(organized))
                self.stat_skipped.config(text=str(skipped))
                self.status_label.config(text=f"Processing {index} of {total}...")
                self.update_idletasks()
        finally:
            self.organize_btn.config(state="normal")
            self.select_btn.config(state="normal")
            self.clear_btn.config(state="normal")

        self.status_label.config(
            text=f"Successfully organized {organized} files.",
            fg=self.colors["success"],
        )
        messagebox.showinfo(
            "Done",
            f"Successfully organized {organized} files.\n\n"
            f"Total: {total}\nOrganized: {organized}\nSkipped: {skipped}",
        )


def main():
    try:
        app = SmartFileOrganizer()
        app.mainloop()
    except Exception as exc:
        # Last-resort catch so the process does not crash silently
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Fatal Error", f"The application failed to start:\n{exc}")
        root.destroy()


if __name__ == "__main__":
    main()
