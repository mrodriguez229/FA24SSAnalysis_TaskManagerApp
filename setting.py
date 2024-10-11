import tkinter as tk

class TaskManagerApp(tk.Tk):
    """
    Main application class for the Task Manager app, managing windows and themes.
    """
    def __init__(self):
        """
        Initializes the main window, sets up the pages, and applies the default theme.
        """
        super().__init__()  # Initialize the parent class (Tk)
        self.title("Task Manager")  # Set window title
        self.geometry("1024x768")  # Set window size
        
        container = tk.Frame(self)  # Create a container frame for the pages
        container.pack(side="top", fill="both", expand=True)  # Configure layout
        
        self.frames = {}  # Store page frames in a dictionary
        for F in (DashboardPage, MyTasksPage, SettingsPage):  # Loop through pages
            page_name = F.__name__  # Get page name
            frame = F(parent=container, controller=self)  # Create page instance
            self.frames[page_name] = frame  # Add to frames dictionary
            frame.grid(row=0, column=0, sticky="nsew")  # Position page in grid
        
        self.theme = "light"  # Default theme
        self.themes = {  # Theme options for light and dark modes
            "light": {"bg": "#d3d3d3", "fg": "#000000"},  # Light theme
            "dark": {"bg": "#333333", "fg": "#FFFFFF"}  # Dark theme
        }
        self.show_frame("DashboardPage")  # Show the dashboard page by default

    def show_frame(self, page_name):
        """
        Displays the specified page.

        Parameters:
        page_name (str): The name of the page to show.
        """
        frame = self.frames[page_name]  # Get the requested page frame
        frame.tkraise()  # Bring the page to the front
        frame.update_theme(self.theme)  # Apply the current theme to the page

    def apply_theme(self, theme):
        """
        Applies the selected theme to all pages.

        Parameters:
        theme (str): The name of the theme to apply (e.g., 'light', 'dark').
        """
        self.theme = theme  # Set the new theme
        for frame in self.frames.values():  # Loop through all pages
            frame.update_theme(theme)  # Update the theme for each page

class DashboardPage(tk.Frame):
    """
    Dashboard page class displaying the main dashboard.
    """
    def __init__(self, parent, controller):
        """
        Initializes the dashboard page.

        Parameters:
        parent (tk.Widget): The parent container.
        controller (TaskManagerApp): The controller to manage navigation and themes.
        """
        tk.Frame.__init__(self, parent)  # Initialize the parent class
        self.controller = controller  # Reference to the controller
        
        label = tk.Label(self, text="Dashboard", font=("Helvetica", 24))  # Create a dashboard label
        label.pack(pady=10)  # Add padding to the label
        
        # Button to navigate to My Tasks page
        button = tk.Button(self, text="Go to My Tasks", command=lambda: controller.show_frame("MyTasksPage"))
        button.pack()

    def update_theme(self, theme):
        """
        Updates the dashboard theme.

        Parameters:
        theme (str): The name of the theme to apply.
        """
        self.config(bg=self.controller.themes[theme]["bg"])  # Update background color

class MyTasksPage(tk.Frame):
    """
    My Tasks page class displaying the task list.
    """
    def __init__(self, parent, controller):
        """
        Initializes the My Tasks page.

        Parameters:
        parent (tk.Widget): The parent container.
        controller (TaskManagerApp): The controller to manage navigation and themes.
        """
        tk.Frame.__init__(self, parent)  # Initialize the parent class
        self.controller = controller  # Reference to the controller
        
        label = tk.Label(self, text="My Tasks", font=("Helvetica", 24))  # Create a label for My Tasks
        label.pack(pady=10)  # Add padding to the label

    def update_theme(self, theme):
        """
        Updates the theme of the My Tasks page.

        Parameters:
        theme (str): The name of the theme to apply.
        """
        self.config(bg=self.controller.themes[theme]["bg"])  # Update background color

class SettingsPage(tk.Frame):
    """
    Settings page class for adjusting application settings, such as themes.
    """
    def __init__(self, parent, controller):
        """
        Initializes the settings page with options for theme changes.

        Parameters:
        parent (tk.Widget): The parent container.
        controller (TaskManagerApp): The controller to manage navigation and themes.
        """
        tk.Frame.__init__(self, parent)  # Initialize the parent class
        self.controller = controller  # Reference to the controller
        
        label = tk.Label(self, text="Settings", font=("Helvetica", 24))  # Create a settings label
        label.pack(pady=10)  # Add padding to the label
        
        # Radio buttons for selecting themes
        self.theme_var = tk.StringVar(value="light")  # Variable to store the selected theme
        
        # Light theme radio button
        light_rb = tk.Radiobutton(self, text="Light Theme", variable=self.theme_var, value="light", command=self.set_theme)
        light_rb.pack(pady=5)
        
        # Dark theme radio button
        dark_rb = tk.Radiobutton(self, text="Dark Theme", variable=self.theme_var, value="dark", command=self.set_theme)
        dark_rb.pack(pady=5)

    def set_theme(self):
        """
        Applies the selected theme.
        """
        self.controller.apply_theme(self.theme_var.get())  # Apply the selected theme

    def update_theme(self, theme):
        """
        Updates the theme of the settings page.

        Parameters:
        theme (str): The name of the theme to apply.
        """
        self.config(bg=self.controller.themes[theme]["bg"])  # Update background color

if __name__ == "__main__":
    app = TaskManagerApp()  # Create the main app instance
    app.mainloop()  # Start the Tkinter main loop
