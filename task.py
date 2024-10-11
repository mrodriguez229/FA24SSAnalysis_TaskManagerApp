import sqlite3

class Task:
    """
    Represents a task in the task management app with title, description, due date, priority, status, and category.
    """
    
    def __init__(self, title, description, due_date, priority, status, category):
        """
        Initializes a task with the provided details.

        Parameters:
        title (str): Task title.
        description (str): Task description.
        due_date (str): Task due date.
        priority (str): Task priority (e.g., High, Medium, Low).
        status (str): Task status (e.g., Pending, Completed).
        category (str): Task category.
        """
        self.title = title  # Title of the task
        self.description = description  # Task description
        self.due_date = due_date  # Task due date
        self.priority = priority  # Task priority
        self.status = status  # Task status
        self.category = category  # Task category
    
    def save(self, task_id):
        """
        Saves or updates the task in the database.

        Parameters:
        task_id (int): ID of the task to update.
        """
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()  # Create a cursor to execute SQL commands
            
            # Update task in the database
            cursor.execute('''
                UPDATE tasks 
                SET title = ?, description = ?, due_date = ?, priority = ?, status = ?
                WHERE id = ?
            ''', (self.title, self.description, self.due_date, self.priority, self.status, task_id))
            
            conn.commit()  # Save changes to the database
    
    def delete(self, task_id):
        """
        Deletes a task from the database.

        Parameters:
        task_id (int): ID of the task to delete.
        """
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()  # Create a cursor to execute SQL commands
            
            # Delete task from the database
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            
            conn.commit()  # Save changes to the database
