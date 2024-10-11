import sqlite3

class Task:
    """
    Represents a task in the task management application. 
    Each task contains a title, description, due date, priority, status, and category.
    """
    
    def __init__(self, title, description, due_date, priority, status, category):
        """
        Initializes a Task object with the provided details.

        Parameters:
        title (str): The title of the task.
        description (str): A brief description of the task.
        due_date (str): The due date of the task.
        priority (str): The priority level of the task (e.g., High, Medium, Low).
        status (str): The current status of the task (e.g., Pending, Completed).
        category (str): The category this task belongs to.
        """
        self.title = title  # Task title
        self.description = description  # Task description
        self.due_date = due_date  # Task due date
        self.priority = priority  # Task priority level
        self.status = status  # Task current status
        self.category = category  # Task category
    
    def save(self, task_id):
        """
        Saves/updates the current task details in the database.

        Parameters:
        task_id (int): The unique identifier of the task to be updated.
        """
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()  # Create a database cursor for executing SQL commands
            
            # Update the task details in the tasks table
            cursor.execute('''
                UPDATE tasks 
                SET title = ?, description = ?, due_date = ?, priority = ?, status = ?
                WHERE id = ?
            ''', (self.title, self.description, self.due_date, self.priority, self.status, task_id))
            
            conn.commit()  # Commit the changes to the database
    
    def delete(self, task_id):
        """
        Deletes a task from the database.

        Parameters:
        task_id (int): The unique identifier of the task to be deleted.
        """
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()  # Create a database cursor for executing SQL commands
            
            # Delete the task from the tasks table
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            
            conn.commit()  # Commit the deletion to the database
