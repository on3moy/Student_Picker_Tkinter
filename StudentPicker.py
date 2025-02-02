import tkinter as tk
import random
import pandas as pd
from PIL import Image, ImageTk
import os

# Students already picked
PICKED = []
# Student List
ALL_STUDENTS = []
BACKGROUND_IMG_PATH = 'img/trex_icon.png'

# Color Scheme
bg_color = '#2a2d33'
fg_color = '#a9dc76'
button_color = '#78dce8'
button_pressed_color = '#8c97f2'

# Create a class
root = tk.Tk()

# Create a title for window
root.title('Student Picker')
root.geometry('400x300')
# Change window color
root.configure(bg=bg_color)

# Load background image
bg_image = Image.open(BACKGROUND_IMG_PATH)
bg_img_resized = bg_image.resize((100, 100))
bg_img_tk = ImageTk.PhotoImage(bg_img_resized)

# Create label to display image
# Add BG color to every label to match background
background_label = tk.Label(root, image=bg_img_tk, bg=bg_color)
# Place image on screen
background_label.place(relx=1, rely=1, anchor='se')

# Add Title Label!
title_label = tk.Label(root, text='Random Student Picker', font=('Consolas', 20, 'bold'), fg=fg_color, bg=bg_color)
title_label.place(relx=.5, rely=.15, anchor='center')

# Add a Button to pick student
pick_student_button = tk.Button(root, text='Pick a Student', font=('Consolas', 14, 'bold'), relief='raised', bg=button_color, activebackground=button_pressed_color)
pick_student_button.place(relx=.5, rely=.35, anchor='center')

# Add Student Name 
student_name_label = tk.Label(root, text='🦖', bg=bg_color, fg='white', font=('Consolas', 30, 'bold'))
student_name_label.place(relx=.5, rely=.55, anchor='center')

# Add File Name
file_name_label = tk.Label(root, text='No File Selected', bg=bg_color, fg='white', font=('Consolas', 8, 'bold'))
file_name_label.place(relx=0, rely=1, anchor='sw')

# Function to change student name
def pick_student():
    global ALL_STUDENTS
    global PICKED

    # Check if you cycled through all the students
    if ALL_STUDENTS:
        if len(ALL_STUDENTS) == len(PICKED):
            # Reset picked list
            PICKED = []
        else:
            # Grab only students that have not been picked
            temp_selection = [x for x in ALL_STUDENTS if x not in PICKED]
            random_student = random.choice(temp_selection)
            student_name_label.config(text=f'{random_student}')
            PICKED.append(random_student)
    else:
        student_name_label.config(text=f'Emtpy List!')

# Add function to button
pick_student_button.config(command=pick_student)

# Add a function to open a window for the list view
# Add a global variable to ensure window does not pop up again
file_window = None

def open_file_selector():
    global file_window
    global ALL_STUDENTS
    global PICKED

    # Every time you pick a new file, reset lists
    ALL_STUDENTS = []
    PICKED = []

    # Logic to bring forth window if it already exists
    if file_window is not None and file_window.winfo_exists():
        file_window.lift()
        return
    
    # State window properties
    file_window = tk.Toplevel(root)
    file_window.title('Select File!')
    file_window.geometry('300x300')
    file_window.configure(bg=bg_color)

    # Add the list box
    list_box = tk.Listbox(file_window, font=('Consolas', 8), background=bg_color, foreground=fg_color)
    list_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Add current files to the list
    for file in os.listdir():
        list_box.insert(tk.END, file)

    # Get selected info
    # Need to put event in for bind to work correctly
    def double_click(event):
        global file_window
        global ALL_STUDENTS
        global PICKED

        # Grab selected file
        selected_file = list_box.curselection()
        if selected_file:
            file_name = list_box.get(selected_file[0])
            file_name_label.config(text=file_name)

            # Try to load csv into list
            try:
                df = pd.read_csv(file_name, header=None, usecols=[0])
                student_names = df.iloc[:, 0].to_list()
                ALL_STUDENTS.extend(student_names)

            except Exception as e:
                file_name_label.config(text='File could not be parsed!')

            file_window.destroy()
            file_window = None
    
    # Create the double click event
    list_box.bind('<Double-Button-1>', double_click)


# Add button to pick data from file
file_picker_button = tk.Button(root, text='Select File', font=('Consolas', 8, 'bold'), relief='raised', bg=button_color, activebackground=button_pressed_color)
file_picker_button.place(relx=.5, rely=.8, anchor='center')
file_picker_button.config(command=open_file_selector)

# Run tkinter event loop
root.mainloop()