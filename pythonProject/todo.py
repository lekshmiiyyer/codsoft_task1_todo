import streamlit as st
from datetime import datetime
# st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)
class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task, deadline):
        self.tasks.append({'task': task, 'deadline': deadline, 'completed': False})

    def list_tasks(self):
        return self.tasks

    def update_task_status(self, task_number, completed):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1]['completed'] = completed

    def update_task(self, task_number, new_task, new_deadline):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1]['task'] = new_task
            self.tasks[task_number - 1]['deadline'] = new_deadline

    def delete_task(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks.pop(task_number - 1)

# Ensure the ToDoList is stored in session state
if 'todo_list' not in st.session_state:
    st.session_state['todo_list'] = ToDoList()

# Get the todo_list from session state
todo_list = st.session_state['todo_list']

# Streamlit App
def main():
    st.title("To-Do List Application")

    # Add Task
    st.header("Add a new task")
    new_task = st.text_input("Enter a task", key='new_task')
    deadline = st.date_input("Deadline", min_value=datetime.today(), key='deadline')
    if st.button("Add Task"):
        if new_task:
            todo_list.add_task(new_task, deadline)
            st.success(f"Added task: {new_task}")
            # st.write('<img src="loading.gif">', unsafe_allow_html=True)
            # st.experimental_rerun()
    # List Tasks
    st.header("Current tasks")
    tasks = todo_list.list_tasks()
    if tasks:
        for i, task in enumerate(tasks, 1):
            status = "✓" if task['completed'] else "✗"
            completed = st.checkbox(f"{i}. [{status}] {task['task']} (Deadline: {task['deadline']})", value=task['completed'], key=f'task_{i}')
            if completed != task['completed']:
                todo_list.update_task_status(i, completed)
    else:
        st.write("No tasks yet!")

    if tasks:
        # Update Task
        st.header("Update a task")
        task_to_update = st.number_input("Enter task number to update", min_value=1, max_value=len(tasks), step=1, key='update_task_number')
        new_task_value = st.text_input("Enter new task description", key='new_task_description')
        new_deadline_value = st.date_input("Enter new deadline", min_value=datetime.today(), key='new_deadline')
        if st.button("Update Task"):
            if new_task_value:
                todo_list.update_task(task_to_update, new_task_value, new_deadline_value)
                st.success(f"Task {task_to_update} updated")
            else:
                st.error("New task description cannot be empty")

        # Delete Task
        st.header("Delete a task")
        task_to_delete = st.number_input("Enter task number to delete", min_value=1, max_value=len(tasks), step=1, key='delete_task_number')
        if st.button("Delete Task"):
            todo_list.delete_task(task_to_delete)
            st.success(f"Task {task_to_delete} deleted")

if __name__ == "__main__":
    main()

