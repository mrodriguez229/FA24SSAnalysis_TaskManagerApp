import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
from tasks import add_task, get_tasks, delete_task, update_task
from task import Task
import datetime
import hashlib
from PIL import Image, ImageTk

class TaskInputFrame(tk.Frame):
    """
    A frame used for inputting task details such as title, description, due date, priority, status, and category.
    """

    def __init__(self, parent, controller, theme, style, update_task_display_callback, *args, **kwargs):
        """
        Initializes the TaskInputFrame with input fields for task details.

        Parameters:
        parent (tk.Widget): The parent widget.
        controller (tk.Widget): The main application controller.
        theme (dict): The current theme being applied.
        style (ttk.Style): The styling options for the widgets.
        update_task_display_callback (callable): Callback function to update the task display.
        """
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.theme = theme
        self.style = style
        self.update_task_display_callback = update_task_display_callback
        self.configure(bg=theme["bg"])  # Set background color based on the theme

        # Task Title Input
        task_title_frame = tk.Frame(self, bg=theme["bg"])
        task_title_frame.pack(fill="x", padx=20, pady=5)
        self.task_title_label = tk.Label(task_title_frame, text="Task Title", font=("Arial", 12), width=15, anchor="w", bg=theme["bg"], fg=theme["fg"])
        self.task_title_label.pack(side="left")
        self.title_entry = tk.Entry(task_title_frame, width=35, bg="white", fg="black")
        self.title_entry.pack(side="left", padx=10)

        # Task Description Input
        task_desc_frame = tk.Frame(self, bg=theme["bg"])
        task_desc_frame.pack(fill="x", padx=20, pady=5)
        self.task_desc_label = tk.Label(task_desc_frame, text="Task Description", font=("Arial", 12), width=15, anchor="w", bg=theme["bg"], fg=theme["fg"])
        self.task_desc_label.pack(side="left")
        self.desc_text = tk.Text(task_desc_frame, height=5, width=35, bg="white", fg="black")
        self.desc_text.pack(side="left", padx=10)

        # Task Category Input
        task_category_frame = tk.Frame(self, bg=theme["bg"])
        task_category_frame.pack(fill="x", padx=20, pady=5)
        self.task_category_label = tk.Label(task_category_frame, text="Category", font=("Arial", 12), width=15, anchor="w", bg=theme["bg"], fg=theme["fg"])
        self.task_category_label.pack(side="left")
        self.category_combobox = ttk.Combobox(task_category_frame, values=["Work", "School", "Personal", "Home", "Other"], state="readonly", width=33, style="TCombobox")
        self.category_combobox.set("Select Category")
        self.category_combobox.pack(side="left", padx=10)

        # Task Due Date Input
        task_due_date_frame = tk.Frame(self, bg=theme["bg"])
        task_due_date_frame.pack(fill="x", padx=20, pady=5)
        self.task_due_date_label = tk.Label(task_due_date_frame, text="Due Date", font=("Arial", 12), width=15, anchor="w", bg=theme["bg"], fg=theme["fg"])
        self.task_due_date_label.pack(side="left")
        self.due_date_entry = DateEntry(task_due_date_frame, width=20, background=theme["bg"], foreground=theme["fg"])
        self.due_date_entry.pack(side="left", padx=10)

        # Task Priority Input
        task_priority_frame = tk.Frame(self, bg=theme["bg"])
        task_priority_frame.pack(fill="x", padx=20, pady=5)
        self.task_priority_label = tk.Label(task_priority_frame, text="Priority", font=("Arial", 12), width=15, anchor="w", background=theme["bg"], foreground=theme["fg"])
        self.task_priority_label.pack(side="left")
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_options = ttk.Combobox(task_priority_frame, textvariable=self.priority_var, values=["Low", "Medium", "High"], state="readonly", width=33, style="TCombobox")
        self.priority_options.pack(side="left", padx=10)

        # Task Status Input
        task_status_frame = tk.Frame(self, bg=theme["bg"])
        task_status_frame.pack(fill="x", padx=20, pady=5)
        self.task_status_label = tk.Label(task_status_frame, text="Status", font=("Arial", 12), width=15, anchor="w", background=theme["bg"], foreground=theme["fg"])
        self.task_status_label.pack(side="left")
        self.status_var = tk.StringVar(value="Pending")
        self.status_options = ttk.Combobox(task_status_frame, textvariable=self.status_var, values=["Pending", "In Progress", "Completed"], state="readonly", width=33, style="TCombobox")
        self.status_options.pack(side="left", padx=10)

        # Create Task Button
        self.create_task_button = tk.Button(self, text="Create Task", font=("Arial", 12), width=20, command=self.create_task, bg=theme["bg"], fg=theme["fg"], relief="raised", bd=2)
        self.create_task_button.pack(pady=20)

    def update_theme(self, theme):
        """
        Updates the current theme for the frame and its widgets.
        Parameters:
        theme (dict): The theme to apply to the widgets.
        """
        self.controller.apply_theme_to_widgets(theme, self.task_title_label, self.task_desc_label, self.task_category_label, self.task_due_date_label, self.task_priority_label, self.task_status_label, self.create_task_button)

    def is_valid_date(self, date_str):
        """
        Validates if the date string is in the correct format (MM/DD/YY).
        Returns True if valid, False otherwise.
        """
        try:
            # Ensure the date follows the correct format
            datetime.datetime.strptime(date_str, '%m/%d/%y')
            return True
        except ValueError:
            return False
    
    def create_task(self):
        """
        Gathers task input data and attempts to create a new task in the system.
        If any validation fails, an error message is shown.
        """
        task_title = self.title_entry.get().strip()  # Task title input
        task_desc = self.desc_text.get("1.0", tk.END).strip()  # Task description input
        task_category = self.category_combobox.get().strip()  # Task category input
        task_due_date = self.due_date_entry.get().strip()  # Task due date input
        task_priority = self.priority_var.get().strip()  # Task priority input
        task_status = self.status_var.get().strip()  # Task status input

        # Input validation
        if not task_title:
            messagebox.showerror("Input Error", "Task title cannot be empty!")
            return
        if not task_due_date:
            messagebox.showerror("Input Error", "Due date cannot be empty!")
            return
        if not self.is_valid_date(task_due_date):
            messagebox.showerror("Input Error", "Invalid date format. Please use MM/DD/YY. Example: 12/31/24.")
            return
        if not task_category:
            messagebox.showerror("Input Error", "Please select a category.")
            return
        if not task_priority:
            messagebox.showerror("Input Error", "Please select a priority level.")
            return
        if not task_status:
            messagebox.showerror("Input Error", "Please select a status.")
            return

        try:
            # Create new task object and save it
            new_task = Task(task_title, task_desc, task_due_date, task_priority, task_status, task_category)
            add_task(new_task)
            self.clear_inputs()  # Clear input fields after creating task
            self.update_task_display_callback()  # Update task list display
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create task: {e}")  # Show error message if task creation fails

    def clear_inputs(self):
        """Clears all input fields after task creation."""
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.category_combobox.set("Select Category")
        self.due_date_entry.set_date(datetime.datetime.now())  # Reset to current date
        self.priority_var.set("Medium")
        self.status_var.set("Pending")


class DashboardFrame(tk.Frame):
    """
    A frame used for displaying the list of tasks and handling task-related actions on the dashboard.
    """

    def __init__(self, parent, theme, style, *args, **kwargs):
        """
        Initializes the DashboardFrame with a list of tasks and a scrollbar for navigation.

        Parameters:
        parent (tk.Widget): The parent widget.
        theme (dict): The current theme being applied.
        style (ttk.Style): The styling options for the widgets.
        """
        super().__init__(parent, *args, **kwargs)
        self.theme = theme  # Current theme applied
        self.style = style  # Styling options for ttk widgets
        self.configure(bg=theme["bg"])  # Set the background color based on the theme

        # Frame for task list display
        self.my_tasks_frame = tk.Frame(self, bg=theme["bg"])
        self.my_tasks_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar for the task list
        self.my_tasks_scrollbar = tk.Scrollbar(self.my_tasks_frame)
        self.my_tasks_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox for displaying tasks
        self.my_tasks_listbox = tk.Listbox(self.my_tasks_frame, yscrollcommand=self.my_tasks_scrollbar.set, width=50, height=10)
        self.my_tasks_listbox.pack(fill="both", expand=True)
        self.my_tasks_scrollbar.config(command=self.my_tasks_listbox.yview)

        self.update_my_tasks()  # Populate the task list

    def update_my_tasks(self):
        """
        Updates the list of tasks displayed in the listbox by fetching tasks from the database.
        """
        self.my_tasks_listbox.delete(0, tk.END)  # Clear the current listbox
        tasks = get_tasks()  # Fetch all tasks
        self.displayed_tasks = sorted(tasks, key=lambda task: datetime.datetime.strptime(task[3], '%m/%d/%y'))  # Sort tasks by due date
        
        # Insert each task into the listbox
        for task in self.displayed_tasks:
            task_info = f"{task[1]} - Due: {task[3]} - Priority: {task[4]}"
            self.my_tasks_listbox.insert(tk.END, task_info)
        
        self.my_tasks_listbox.bind("<Double-1>", self.open_task_window)  # Bind double-click to open task window

    def open_task_window(self, event):
        """
        Opens a new window to edit or delete the selected task.

        Parameters:
        event (tk.Event): The event object when a task is selected from the listbox.
        """
        selected_index = self.my_tasks_listbox.curselection()  # Get selected task index
        if selected_index:
            selected_index = selected_index[0]
            selected_task = self.displayed_tasks[selected_index]
            self.show_edit_task_window(selected_task)  # Open the edit task window

    def show_edit_task_window(self, task):
        """
        Displays a window that allows the user to edit or delete the selected task.
        """
        edit_window = tk.Toplevel(self)  # Create a new window for editing the task
        edit_window.title("Edit Task")
        window_width, window_height = 700, 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))  # Center the window on the screen
        y = int((screen_height / 2) - (window_height / 2))
        edit_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Apply theme to the window
        edit_window.configure(bg=self.theme["bg"])

        # Task Title
        title_label = tk.Label(edit_window, text="Task Title", bg=self.theme["bg"], fg=self.theme["fg"])
        title_label.pack(pady=5)
        title_entry = tk.Entry(edit_window, bg=self.theme["entry_bg"], fg=self.theme["entry_fg"])
        title_entry.pack(pady=5)
        title_entry.insert(0, task[1])

        # Task Description
        desc_label = tk.Label(edit_window, text="Task Description", bg=self.theme["bg"], fg=self.theme["fg"])
        desc_label.pack(pady=5)
        desc_text = tk.Text(edit_window, height=5, bg=self.theme["entry_bg"], fg=self.theme["entry_fg"])
        desc_text.pack(pady=5)
        desc_text.insert(tk.END, task[2])

        # Due Date
        due_date_label = tk.Label(edit_window, text="Due Date", bg=self.theme["bg"], fg=self.theme["fg"])
        due_date_label.pack(pady=5)
        due_date_entry = DateEntry(edit_window, background=self.theme["bg"], foreground=self.theme["fg"])
        due_date_entry.pack(pady=5)
        due_date_entry.set_date(task[3])

        # Priority
        priority_label = tk.Label(edit_window, text="Priority", bg=self.theme["bg"], fg=self.theme["fg"])
        priority_label.pack(pady=5)
        priority_var = tk.StringVar(value=task[4])
        priority_options = ttk.Combobox(edit_window, textvariable=priority_var, values=["Low", "Medium", "High"], state="readonly")
        priority_options.pack(pady=5)

        # Status
        status_label = tk.Label(edit_window, text="Status", bg=self.theme["bg"], fg=self.theme["fg"])
        status_label.pack(pady=5)
        status_var = tk.StringVar(value=task[5])
        status_options = ttk.Combobox(edit_window, textvariable=status_var, values=["Pending", "In Progress", "Completed"], state="readonly")
        status_options.pack(pady=5)

        # Category
        category_label = tk.Label(edit_window, text="Category", bg=self.theme["bg"], fg=self.theme["fg"])
        category_label.pack(pady=5)
        category_var = tk.StringVar(value=task[6])
        category_combobox = ttk.Combobox(edit_window, textvariable=category_var, values=["Work", "School", "Personal", "Home", "Other"], state="readonly")
        category_combobox.pack(pady=5)

        # Button to save changes to the task
        save_button = tk.Button(edit_window, text="Save Changes", bg=self.theme["bg"], fg=self.theme["fg"], command=lambda: self.save_edited_task(task[0], title_entry.get(), desc_text.get("1.0", tk.END), due_date_entry.get(), priority_var.get(), status_var.get(), category_var.get(), edit_window))
        save_button.pack(pady=10)

        # Button to delete the task
        delete_button = tk.Button(edit_window, text="Delete Task", bg=self.theme["bg"], fg=self.theme["fg"], command=lambda: self.delete_task_and_close(task[0], edit_window))
        delete_button.pack(pady=10)

        # Store references to the window and its widgets (including labels)
        self.edit_window = edit_window
        self.edit_widgets = [title_label, title_entry, desc_label, desc_text, due_date_label, due_date_entry, 
                         priority_label, priority_options, status_label, status_options, category_label, 
                         category_combobox, save_button, delete_button]

    def save_edited_task(self, task_id, title, description, due_date, priority, status, category, edit_window):
        """
        Saves the changes made to the task and updates the task list.

        Parameters:
        task_id (int): The ID of the task to update.
        title (str): The updated task title.
        description (str): The updated task description.
        due_date (str): The updated due date.
        priority (str): The updated priority level.
        status (str): The updated task status.
        category (str): The updated task category.
        edit_window (tk.Toplevel): The window where the task is edited.
        """
        updated_task = Task(title, description, due_date, priority, status, category)  # Create an updated Task object
        update_task(updated_task, task_id)  # Update the task in the database
        self.update_my_tasks()  # Refresh the task list
        edit_window.destroy()  # Close the edit window

    def delete_task_and_close(self, task_id, window):
        """
        Deletes the selected task and closes the edit window.

        Parameters:
        task_id (int): The ID of the task to delete.
        window (tk.Toplevel): The window where the task is being edited.
        """
        response = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")  # Confirmation dialog
        if response:
            delete_task(task_id)  # Delete the task from the database
            window.destroy()  # Close the edit window
            self.update_my_tasks()  # Refresh the task list


class TaskManagerApp(tk.Tk):
    """
    The main application class for the Task Manager app. Manages navigation between pages, user login, and theme switching.
    """

    def __init__(self):
        """
        Initializes the main application window, frames (pages), sidebar, topbar, and applies the default theme.
        """
        super().__init__()
        self.title("Task Manager")  # Set the title of the window
        self.geometry("700x600")  # Set the window size
        self.theme = "light"  # Default theme for the application
        self.themes = {  # Theme settings for light and dark modes
            "light": {"bg": "#d3d3d3", "fg": "#000000", "entry_bg": "#FFFFFF", "entry_fg": "#000000"},
            "dark": {"bg": "#333333", "fg": "#FFFFFF", "entry_bg": "#444444", "entry_fg": "#FFFFFF"}
        }
        self.style = ttk.Style()  # Style for ttk widgets
        self.mode_var = tk.StringVar(value="Light Mode")  # Variable to switch between light and dark modes
        self.frames = {}  # Dictionary to hold the frames (pages)
        self.logged_in = False  # Flag to track if the user is logged in

        # Create various sections of the application
        self.create_sidebar()  # Create the sidebar with navigation buttons
        self.create_topbar()  # Create the top bar with login and add task buttons
        self.create_main_page()  # Create the main page with the calendar
        self.create_my_tasks_page()  # Create the My Tasks page
        self.create_settings_page()  # Create the Settings page
        self.create_add_task_page()  # Create the Add Task page
        self.apply_theme()  # Apply the default theme
        self.show_frame("MainPage")  # Show the main page by default

    def create_sidebar(self):
        """
        Creates the sidebar with navigation buttons for different pages.
        """
        self.sidebar = tk.Frame(self, bg=self.themes[self.theme]["bg"], width=200, bd=2, relief="ridge")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)

        # Add logo and buttons to the sidebar
        logo_image = tk.PhotoImage(file="assets/logo.png").subsample(3, 3)
        self.logo_label = tk.Label(self.sidebar, image=logo_image, bg=self.themes[self.theme]["bg"], bd=0)
        self.logo_label.image = logo_image  # Store reference to the image
        self.logo_label.pack(pady=(10, 20))

        # Define button style
        button_style = {"width": 15, "height": 1, "bg": self.themes[self.theme]["bg"], "fg": self.themes[self.theme]["fg"], "relief": "raised", "bd": 2, "anchor": "center"}
        
        # Create sidebar buttons
        self.dashboard_button = tk.Button(self.sidebar, text="Dashboard", **button_style, command=lambda: self.show_frame("MainPage"))
        self.dashboard_button.pack(padx=10, pady=10, fill=tk.X)
        
        self.tasks_button = tk.Button(self.sidebar, text="My Tasks", **button_style, command=self.open_tasks_page)
        self.tasks_button.pack(padx=10, pady=10, fill=tk.X)
        
        self.settings_button = tk.Button(self.sidebar, text="Settings", **button_style, command=lambda: self.show_frame("SettingsPage"))
        self.settings_button.pack(padx=10, pady=10, fill=tk.X)

        # Log out button at the bottom of the sidebar
        self.spacer = tk.Frame(self.sidebar, bg=self.themes[self.theme]["bg"])
        self.spacer.pack(expand=True, fill=tk.Y, pady=0)
        self.logout_button = tk.Button(self.sidebar, text="Log Out", **button_style, command=self.log_out)
        self.logout_button.pack(padx=10, pady=10, fill=tk.X)

    def create_topbar(self):
        """
        Creates the top bar with login and add task buttons.
        """
        self.top_frame = tk.Frame(self, bg=self.themes[self.theme]["bg"], height=50, bd=2, relief="ridge")
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)

        # Create login button with an image
        button_style = {"width": 15, "height": 1, "bg": self.themes[self.theme]["bg"], "fg": self.themes[self.theme]["fg"], "relief": "raised", "bd": 2, "anchor": "center"}
        login_image_path = "assets/login.png"
        login_image = Image.open(login_image_path)
        login_image = login_image.resize((100, 90), Image.LANCZOS)
        self.login_photo = ImageTk.PhotoImage(login_image)
        self.login_button = tk.Button(self.top_frame, image=self.login_photo, command=self.open_login_window, bg=self.themes[self.theme]["bg"], borderwidth=0, highlightthickness=0, relief="flat")
        self.login_button.pack(side=tk.RIGHT, padx=10, pady=0)

        # Create add task button
        self.add_task_button = tk.Button(self.top_frame, text="+ Add Task", **button_style, command=lambda: self.show_frame("AddTaskPage"))
        self.add_task_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def create_main_page(self):
        """
        Creates the main page which contains a calendar to display tasks.
        """
        if "MainPage" not in self.frames:
            self.main_frame = tk.Frame(self, bg=self.themes[self.theme]["bg"], bd=2, relief="ridge")
            self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
            calendar_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=1, relief="solid")
            calendar_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.8)
            
            today = datetime.datetime.now()  # Get today's date
            self.calendar = Calendar(calendar_frame, selectmode='day', year=today.year, month=today.month, day=today.day)  # Create the calendar widget
            self.calendar.pack(expand=True, fill="both")

            self.frames["MainPage"] = self.main_frame  # Store reference to the main page
        else:
            self.clear_calendar_tasks()  # Clear tasks if already initialized

        if self.logged_in:
            self.update_calendar_tasks()  # Update the calendar with tasks if logged in

    def clear_calendar_tasks(self):
        """
        Clears all tasks displayed on the calendar.
        """
        for event_id in self.calendar.get_calevents():
            self.calendar.calevent_remove(event_id)  # Remove all calendar events

    def update_calendar_tasks(self):
        """
        Updates the calendar by fetching tasks from the database and marking their due dates.
        """
        tasks = get_tasks()  # Fetch all tasks
        for task in tasks:
            due_date_str = task[3]
            due_date = datetime.datetime.strptime(due_date_str, '%m/%d/%y')
            self.calendar.calevent_create(due_date, task[1], 'task_due')  # Add task due date to the calendar
        self.calendar.tag_config('task_due', background='lightblue', foreground='black')  # Configure the calendar event tag

    def open_login_window(self):
        """
        Opens the login window for user authentication.
        """
        login_window = tk.Toplevel(self)  # Create a new login window
        login_window.title("Log In")
        window_width, window_height = 300, 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))  # Center the window on the screen
        y = int((screen_height / 2) - (window_height / 2))
        login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create input fields for username and password
        username_label = tk.Label(login_window, text="Username (max 15 chars):")
        username_label.pack(pady=10)
        username_entry = tk.Entry(login_window)
        username_entry.pack(pady=5)
        username_entry.focus_set()  # Focus on username input

        password_label = tk.Label(login_window, text="Password (8-12 chars):")
        password_label.pack(pady=10)
        password_entry = tk.Entry(login_window, show="*")  # Mask the password input
        password_entry.pack(pady=5)

        # Create the login button
        login_button = tk.Button(login_window, text="Login", command=lambda: self.validate_login(username_entry.get(), password_entry.get(), login_window))
        login_button.pack(pady=10)

    def validate_login(self, username, password, login_window):
        """
        Validates the user login by checking the credentials.

        Parameters:
        username (str): The entered username.
        password (str): The entered password.
        login_window (tk.Toplevel): The login window to be closed after validation.
        """
        users = self.load_users()  # Load the predefined users

        # Perform input validation
        if not username or not password:
            tk.messagebox.showerror("Input Error", "Both username and password are required!")
        elif len(username) > 15:
            tk.messagebox.showerror("Input Error", "Username cannot exceed 15 characters!")
        elif len(password) > 12 or len(password) < 8:
            tk.messagebox.showerror("Input Error", "Password must be between 8-12 characters!")
        elif not username.isalnum():
            tk.messagebox.showerror("Input Error", "Username can only contain letters and numbers!")
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the entered password
            if username in users and users[username] == hashed_password:  # Check if the username and password match
                tk.messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                self.logged_in = True  # Set the logged in flag to True
                self.tasks_button.config(state="normal")  # Enable the tasks button
                self.create_main_page()  # Update the main page
                self.show_frame("MainPage")  # Show the main page
            else:
                tk.messagebox.showerror("Login Failed", "Invalid username or password")

        # Clear the input fields
        for widget in login_window.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
        login_window.destroy()  # Close the login window

    def load_users(self):
        """
        Loads predefined users for authentication.

        Returns:
        dict: A dictionary of users with their hashed passwords.
        """
        return {
            'admin': hashlib.sha256('password123'.encode()).hexdigest(),  # Predefined user 'admin'
            }

    def log_out(self):
        """
        Logs the user out and resets the app state.
        """
        response = messagebox.askyesno("Log Out", "Are you sure you want to log out?")  # Ask for confirmation
        if response:
            self.logged_in = False  # Set the logged in flag to False
            self.clear_calendar_tasks()  # Clear tasks from the calendar
            self.show_frame("MainPage")  # Show the main page
            self.login_button.config(state="normal")  # Re-enable the login button

    def create_my_tasks_page(self):
        """
        Creates the My Tasks page where the user can view and manage their tasks.
        """
        theme = self.themes[self.theme]  # Get the current theme
        self.my_tasks_frame = DashboardFrame(self, self.themes[self.theme], self.style)  # Create the DashboardFrame
        self.my_tasks_frame.config(bg=theme["bg"], bd=2, relief="ridge")
        self.frames["MyTasksPage"] = self.my_tasks_frame
        self.my_tasks_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def open_tasks_page(self):
        """
        Opens the My Tasks page if the user is logged in.
        """
        if self.logged_in:
            self.show_frame("MyTasksPage")  # Show the My Tasks page
        else:
            tk.messagebox.showerror("Access Denied", "You must log in to access this page.")  # Show error if not logged in

    def create_add_task_page(self):
        """
        Creates the Add Task page where users can input and create new tasks.
        """
        theme = self.themes[self.theme]  # Get the current theme
        self.add_task_frame = TaskInputFrame(self, self, self.themes[self.theme], self.style, self.update_tasks_in_my_tasks_page)  # Create TaskInputFrame
        self.add_task_frame.config(bg=theme["bg"], bd=2, relief="ridge")
        self.frames["AddTaskPage"] = self.add_task_frame
        self.add_task_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def create_settings_page(self):
        """
        Creates the Settings page where users can adjust preferences such as the theme.
        """
        self.settings_frame = tk.Frame(self, bg=self.themes[self.theme]["bg"], bd=2, relief="ridge")  # Create settings frame
        self.mode_frame = tk.Frame(self.settings_frame, bg=self.themes[self.theme]["bg"])
        self.mode_frame.pack(pady=10, padx=50, anchor="w")

        # Create label and combobox for theme selection
        self.mode_label = tk.Label(self.mode_frame, text="Select Mode:", font=("Arial", 12), bg=self.themes[self.theme]["bg"], fg=self.themes[self.theme]["fg"])
        self.mode_label.pack(side="left", padx=(0, 10))
        self.mode_button = ttk.Combobox(self.mode_frame, textvariable=self.mode_var, values=["Light Mode", "Dark Mode"], background="white", foreground="black")
        self.mode_button.pack(side="left")
        self.mode_button.bind("<<ComboboxSelected>>", lambda event: self.apply_theme_from_combobox())  # Bind combobox selection event

        self.task_prefs_frame = tk.Frame(self.settings_frame, bg=self.themes[self.theme]["bg"])
        self.task_prefs_frame.pack(pady=10, padx=50, anchor="w")
        self.frames["SettingsPage"] = self.settings_frame  # Store reference to the settings page

    def show_frame(self, frame_name):
        """
        Displays the specified frame (page) in the application.

        Parameters:
        frame_name (str): The name of the frame (page) to display.
        """
        if frame_name in ["MyTasksPage", "AddTaskPage"] and not self.logged_in:
            tk.messagebox.showerror("Access Denied", "You must log in to access this page.")  # Show error if trying to access without logging in
            return

        # Hide all frames and show the requested one
        for frame in self.frames.values():
            frame.pack_forget()

        frame = self.frames.get(frame_name)
        if frame:
            frame.pack(fill="both", expand=True)
            if frame_name == "MainPage":
                today = datetime.datetime.now()
                self.calendar.selection_set(today)  # Set calendar selection to today
        else:
            print(f"Frame '{frame_name}' not found!")  # Print error if frame is not found

    def apply_theme(self):
        self.theme = "light" if self.mode_var.get() == "Light Mode" else "dark"
        current_theme = self.themes[self.theme]

        # Apply theme settings to other sections
        self.sidebar.config(bg=current_theme["bg"], bd=2, relief="ridge")
        self.logo_label.config(bg=current_theme["bg"])
        self.spacer.config(bg=current_theme["bg"])
        self.main_frame.config(bg=current_theme["bg"], bd=2, relief="ridge")
        self.my_tasks_frame.config(bg=current_theme["bg"])
        self.add_task_frame.config(bg=current_theme["bg"])

        # Update task frame theme and apply to widgets
        self.add_task_frame.update_theme(current_theme)
        self.add_task_frame.update_idletasks()

        self.settings_frame.config(bg=current_theme["bg"], bd=2, relief="ridge")
        self.top_frame.config(bg=current_theme["bg"], bd=2, relief="ridge")
        self.mode_frame.config(bg=current_theme["bg"])
        self.mode_label.config(bg=current_theme["bg"], fg=current_theme["fg"])
        self.task_prefs_frame.config(bg=current_theme["bg"])

        # Apply theme to the edit window, if it exists and is open
        if hasattr(self, 'edit_window') and self.edit_window.winfo_exists():
            self.apply_theme_to_edit_window(self.edit_window, self.edit_widgets)

        # Apply theme to sidebar and topbar buttons
        for widget in self.sidebar.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=current_theme["bg"], fg=current_theme["fg"], relief="raised")
        for widget in self.top_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=current_theme["bg"], fg=current_theme["fg"], relief="raised")

        self.style.configure("TCombobox", fieldbackground="white", foreground="black")  # Set combobox styles

    def apply_theme_to_edit_window(self, edit_window, widgets):
        """
        Applies the theme to the edit task window and its widgets.
    
        Parameters:
        edit_window (tk.Toplevel): The edit task window.
        widgets (list): A list of widgets to apply the theme.
        """
        edit_window.configure(bg=self.themes[self.theme]["bg"])
        for widget in widgets:
            widget.configure(bg=self.themes[self.theme]["bg"], fg=self.themes[self.theme]["fg"])

    def apply_theme_from_combobox(self):
        """
        Applies the theme selected from the combobox on the settings page.
        """
        self.apply_theme()  # Call the apply_theme method to update the theme

    def apply_theme_to_widgets(self, theme, *widgets):
        """
        Applies the selected theme to the given widgets.

        Parameters:
        theme (dict): The theme to apply to the widgets.
        widgets (tk.Widget): The widgets to update with the theme.
        """
        for widget in widgets:
            widget.config(bg=theme["bg"], fg=theme["fg"])  # Set the background and foreground color for each widget

    def update_tasks_in_my_tasks_page(self):
        """
        Updates the task list on the My Tasks page by calling the update method of the frame.
        """
        if "MyTasksPage" in self.frames:
            self.my_tasks_frame.update_my_tasks()  # Call the update method of the My Tasks page


if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
