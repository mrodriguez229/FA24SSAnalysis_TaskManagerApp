import tkinter as tk

class TaskManagerApp(tk.Tk):
    """
    Main application class for the Task Manager App, which handles the app's windows and themes.
    """
    def __init__(self):
        """
        Initializes the main application window, sets up the frames (pages), and applies the default theme.
        """
        super().__init__()  # Initialize the parent class (Tk)
        self.title("Task Manager")  # Set the title of the main window
        self.geometry("1024x768")  # Set the size of the window
        
        container = tk.Frame(self)  # Create a container frame to hold different pages
        container.pack(side="top", fill="both", expand=True)  # Configure the frame layout
        
        self.frames = {}  # Dictionary to hold the different page frames
        for F in (DashboardPage, MyTasksPage, SettingsPage):  # Loop through the page classes
            page_name = F.__name__  # Get the name of the page class
            frame = F(parent=container, controller=self)  # Create an instance of the page class
            self.frames[page_name] = frame  # Store the frame in the dictionary
            frame.grid(row=0, column=0, sticky="nsew")  # Position the frame in the grid
        
        self.theme = "light"  # Default theme for the app
        self.themes = {  # Theme settings for light and dark modes
            "light": {"bg": "#d3d3d3", "fg": "#000000"},  # Light theme colors
            "dark": {"bg": "#333333", "fg": "#FFFFFF"}  # Dark theme colors
        }
        self.show_frame("DashboardPage")  # Show the dashboard page by default

    def show_frame(self, page_name):
        """
        Displays the selected page by raising the frame to the front.

        Parameters:
        page_name (str): The name of the page to display.
        """
        frame = self.frames[page_name]  # Retrieve the frame for the requested page
        frame.tkraise()  # Bring the frame to the top
        frame.update_theme(self.theme)  # Apply the current theme to the frame

    def apply_theme(self, theme):
        """
        Applies the selected theme to all frames in the application.

        Parameters:
        theme (str): The name of the theme to apply (e.g., 'light', 'dark').
        """
        self.theme = theme  # Set the new theme
        for frame in self.frames.values():  # Loop through all the frames
            frame.update_theme(theme)  # Update the theme of each frame

class DashboardPage(tk.Frame):
    """
    Dashboard page class for displaying the main dashboard of the app.
    """
    def __init__(self, parent, controller):
        """
        Initializes the dashboard page.

        Parameters:
        parent (tk.Widget): The parent widget (usually the main container).
        controller (TaskManagerApp): The controller class to manage app navigation and themes.
        """
        tk.Frame.__init__(self, parent)  # Initialize the parent class (Frame)
        self.controller = controller  # Store the reference to the controller
        
        label = tk.Label(self, text="Dashboard", font=("Helvetica", 24))  # Create the dashboard label
        label.pack(pady=10)  # Pack the label with padding
        
        # Button to navigate to the My Tasks page
        button = tk.Button(self, text="Go to My Tasks", command=lambda: controller.show_frame("MyTasksPage"))
        button.pack()

    def update_theme(self, theme):
        """
        Updates the theme of the dashboard page.

        Parameters:
        theme (str): The name of the theme to apply (e.g., 'light', 'dark').
        """
        self.config(bg=self.controller.themes[theme]["bg"])  # Set the background color based on the theme

class MyTasksPage(tk.Frame):
    """
    My Tasks page class for displaying the list of tasks.
    """
    def __init__(self, parent, controller):
        """
        Initializes the My Tasks page.

        Parameters:
        parent (tk.Widget): The parent widget (usually the main container).
        controller (TaskManagerApp): The controller class to manage app navigation and themes.
        """
        tk.Frame.__init__(self, parent)  # Initialize the parent class (Frame)
        self.controller = controller  # Store the reference to the controller
        
        label = tk.Label(self, text="My Tasks", font=("Helvetica", 24))  # Create the My Tasks label
        label.pack(pady=10)  # Pack the label with padding

    def update_theme(self, theme):
        """
        Updates the theme of the My Tasks page.

        Parameters:
        theme (str): The name of the theme to apply (e.g., 'light', 'dark').
        """
        self.config(bg=self.controller.themes[theme]["bg"])  # Set the background color based on the theme

class SettingsPage(tk.Frame):
    """
    Settings page class for changing application settings like themes.
    """
    def __init__(self, parent, controller):
        """
        Initializes the settings page with options for changing the theme.

        Parameters:
        parent (tk.Widget): The parent widget (usually the main container).
        controller (TaskManagerApp): The controller class to manage app navigation and themes.
        """
        tk.Frame.__init__(self, parent)  # Initialize the parent class (Frame)
        self.controller = controller  # Store the reference to the controller
        
        label = tk.Label(self, text="Settings", font=("Helvetica", 24))  # Create the Settings label
        label.pack(pady=10)  # Pack the label with padding
        
        # Variable to store the selected theme (light or dark)
        self.theme_var = tk.StringVar(value="light")
        
        # Radio buttons for selecting the light theme
        light_rb = tk.Radiobutton(self, text="Light Theme", variable=self.theme_var, value="light", command=self.set_theme)
        light_rb.pack(pady=5)
        
        # Radio buttons for selecting the dark theme
        dark_rb = tk.Radiobutton(self, text="Dark Theme", variable=self.theme_var, value="dark", command=self.set_theme)
        dark_rb.pack(pady=5)

    def set_theme(self):
        """
        Sets the selected theme by calling the controller to apply it.
        """
        self.controller.apply_theme(self.theme_var.get())  # Apply the selected theme

    def update_theme(self, theme):
        """
        Updates the theme of the settings page.

        Parameters:
        theme (str): The name of the theme to apply (e.g., 'light', 'dark').
        """
        self.config(bg=self.controller.themes[theme]["bg"])  # Set the background color based on the theme

if __name__ == "__main__":
    app = TaskManagerApp()  # Instantiate the main application class
    app.mainloop()  # Start the Tkinter main loop
