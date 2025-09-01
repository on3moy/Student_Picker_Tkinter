import tkinter as tk
from tkinter import messagebox
import random
import pandas as pd
from PIL import Image, ImageTk
import os

# ---------- Themed colors ----------
BG_COLOR = '#2a2d33'
FG_COLOR = '#a9dc76'
BTN_COLOR = '#78dce8'
BTN_ACTIVE = '#8c97f2'

BACKGROUND_IMG_PATH = 'img/trex_icon.png'
FOLDER_NAME = 'student_names'

class StudentPickerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Student Picker')
        self.geometry('480x360')
        self.configure(bg=BG_COLOR)

        # Ensure folder exists
        self.folder_path = os.path.join(os.getcwd(), FOLDER_NAME)
        os.makedirs(self.folder_path, exist_ok=True)

        # Data/state
        self.all_students: list[str] = []
        self.picked: set[str] = set()
        self.file_window = None
        self.list_window = None
        self.bg_img_tk = None

        # --- UI ---
        self._build_ui()
        self._bind_shortcuts()

    # ---------- UI ----------
    def _build_ui(self):
        # Optional background image (bottom-right)
        if os.path.exists(BACKGROUND_IMG_PATH):
            try:
                bg_image = Image.open(BACKGROUND_IMG_PATH).resize((110, 110))
                self.bg_img_tk = ImageTk.PhotoImage(bg_image)
                tk.Label(self, image=self.bg_img_tk, bg=BG_COLOR).place(relx=1, rely=1, anchor='se')
            except Exception:
                pass

        tk.Label(self, text='Random Student Picker',
                 font=('Consolas', 20, 'bold'), fg=FG_COLOR, bg=BG_COLOR).place(relx=.5, rely=.12, anchor='center')

        self.student_name_label = tk.Label(self, text='🦖', bg=BG_COLOR, fg='white', font=('Consolas', 28, 'bold'))
        self.student_name_label.place(relx=.5, rely=.50, anchor='center')

        self.status_label = tk.Label(self, text='Load a CSV from the Student_Names folder.',
                                     bg=BG_COLOR, fg='#cfcfcf', font=('Consolas', 9))
        self.status_label.place(relx=.5, rely=.66, anchor='center')

        # Buttons row
        row = tk.Frame(self, bg=BG_COLOR)
        row.place(relx=.5, rely=.32, anchor='center')

        self.pick_btn = tk.Button(row, text='Pick a Student', font=('Consolas', 14, 'bold'),
                                  relief='raised', bg=BTN_COLOR, activebackground=BTN_ACTIVE,
                                  command=self.pick_student)
        self.pick_btn.pack(side=tk.LEFT, padx=6)

        self.view_btn = tk.Button(row, text='View Lists', font=('Consolas', 12, 'bold'),
                                  relief='raised', bg=BTN_COLOR, activebackground=BTN_ACTIVE,
                                  command=self.open_list_window)
        self.view_btn.pack(side=tk.LEFT, padx=6)

        self.file_btn = tk.Button(self, text='Select File', font=('Consolas', 10, 'bold'),
                                  relief='raised', bg=BTN_COLOR, activebackground=BTN_ACTIVE,
                                  command=self.open_file_selector)
        self.file_btn.place(relx=.5, rely=.80, anchor='center')

        self.reset_btn = tk.Button(self, text='Reset Picks', font=('Consolas', 9, 'bold'),
                                   relief='raised', bg=BTN_COLOR, activebackground=BTN_ACTIVE,
                                   command=self.reset_picks, state=tk.DISABLED)
        self.reset_btn.place(relx=.83, rely=.80, anchor='center')

        self.file_name_label = tk.Label(self, text='No File Selected',
                                        bg=BG_COLOR, fg='white', font=('Consolas', 8, 'bold'))
        self.file_name_label.place(relx=0, rely=1, anchor='sw')

    def _bind_shortcuts(self):
        self.bind('<space>', lambda e: self.pick_student())
        self.bind('<Control-o>', lambda e: self.open_file_selector())
        self.bind('<Control-l>', lambda e: self.open_list_window())
        self.bind('<Control-r>', lambda e: self.reset_picks())

    # ---------- Logic ----------
    def set_status(self, msg: str):
        self.status_label.config(text=msg)

    def reset_picks(self):
        if not self.all_students:
            return
        self.picked.clear()
        self.student_name_label.config(text='—')
        self.set_status('Picks reset.')
        self._refresh_list_window()
        self._update_reset_state()

    def _update_reset_state(self):
        self.reset_btn.config(state=(tk.NORMAL if self.picked else tk.DISABLED))

    def pick_student(self):
        if not self.all_students:
            self.student_name_label.config(text='Empty list!')
            self.set_status('Load a txt first (double-click a file).')
            return

        remaining = [s for s in self.all_students if s not in self.picked]
        if not remaining:
            # soft auto-reset on complete cycle
            self.picked.clear()
            self.set_status('All students were picked. Resetting… Pick again!')
            self._refresh_list_window()
            self._update_reset_state()
            return

        chosen = random.choice(remaining)
        self.picked.add(chosen)
        self.student_name_label.config(text=chosen)
        self.set_status(f'Picked: {chosen}')
        self._refresh_list_window()
        self._update_reset_state()

    def _refresh_list_window(self):
        if not (self.list_window and self.list_window.winfo_exists()):
            return
        # Rebuild the listboxes contents
        self._populate_listboxes()

    def _populate_listboxes(self):
        if not hasattr(self, 'picked_box') or not hasattr(self, 'remaining_box'):
            return
        self.picked_box.delete(0, tk.END)
        for s in sorted(self.picked):
            self.picked_box.insert(tk.END, s)

        self.remaining_box.delete(0, tk.END)
        for s in sorted([x for x in self.all_students if x not in self.picked]):
            self.remaining_box.insert(tk.END, s)

    # ---------- Windows ----------
    def open_list_window(self):
        if self.list_window and self.list_window.winfo_exists():
            self.list_window.lift()
            return
        self.list_window = tk.Toplevel(self)
        self.list_window.title('Picked vs Remaining')
        self.list_window.geometry('360x360')
        self.list_window.configure(bg=BG_COLOR)

        tk.Label(self.list_window, text="Picked",
                 font=('Consolas', 12, 'bold'), bg=BG_COLOR, fg=FG_COLOR).pack(anchor='w', padx=10, pady=(10, 0))
        self.picked_box = tk.Listbox(self.list_window, height=8, width=40, bg=BG_COLOR, fg=FG_COLOR)
        self.picked_box.pack(padx=10, pady=4, fill='both')

        tk.Label(self.list_window, text="Remaining",
                 font=('Consolas', 12, 'bold'), bg=BG_COLOR, fg=FG_COLOR).pack(anchor='w', padx=10, pady=(10, 0))
        self.remaining_box = tk.Listbox(self.list_window, height=8, width=40, bg=BG_COLOR, fg=FG_COLOR)
        self.remaining_box.pack(padx=10, pady=4, fill='both')

        self._populate_listboxes()
        self.list_window.bind('<FocusIn>', lambda e: self._refresh_list_window())

    def open_file_selector(self):
        # If open, just focus
        if self.file_window and self.file_window.winfo_exists():
            self.file_window.lift()
            return

        self.file_window = tk.Toplevel(self)
        self.file_window.title('Select File (double-click)')
        self.file_window.geometry('320x360')
        self.file_window.configure(bg=BG_COLOR)

        info = tk.Label(self.file_window, text=f'Folder: {self.folder_path}',
                        bg=BG_COLOR, fg='#cfcfcf', font=('Consolas', 8))
        info.pack(anchor='w', padx=10, pady=(8,0))

        self.file_list = tk.Listbox(self.file_window, font=('Consolas', 9),
                                    background=BG_COLOR, foreground=FG_COLOR)
        self.file_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        files = [f for f in os.listdir(self.folder_path) if f.lower().endswith('.txt')]
        if not files:
            self.file_list.insert(tk.END, '(No txt files found)')
            self.file_list.config(state=tk.DISABLED)
        else:
            for f in files:
                self.file_list.insert(tk.END, f)

        self.file_list.bind('<Double-Button-1>', self._on_file_double_click)

    def _on_file_double_click(self, event):
        if not self.file_list.cget('state') == tk.NORMAL:
            return
        sel = self.file_list.curselection()
        if not sel:
            return
        fname = self.file_list.get(sel[0])
        fpath = os.path.join(self.folder_path, fname)
        ok = self._load_students_from_txt(fpath)
        if ok:
            self.file_name_label.config(text=fname)
            self.student_name_label.config(text='—')
            self.set_status(f'Loaded {len(self.all_students)} students.')
            self._update_reset_state()
            self._refresh_list_window()
        self.file_window.destroy()
        self.file_window = None

    # ---------- Txt loading ----------
    def _load_students_from_txt(self, path: str) -> bool:
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(
                    f'{os.path.basename(path)} not found in {self.folder_path} folder! '
                    'Please add a .txt file with student names.'
                )

            with open(path, 'r', encoding='utf-8') as file:
                student_names = [line.strip() for line in file if line.strip()]

            if not student_names:
                raise ValueError('The file is empty or contains no valid names.')

            # De-duplicate while preserving order, ignore "name" header if present
            seen = set()
            ordered_unique = []
            for n in student_names:
                if n and n.lower() != 'name' and n not in seen:
                    seen.add(n)
                    ordered_unique.append(n)

            self.all_students = ordered_unique
            self.picked.clear()
            return True

        except Exception as e:
            messagebox.showerror('Load Error', f'Could not parse TXT:\n{e}')
            return False


if __name__ == '__main__':
    app = StudentPickerApp()
    app.mainloop()
