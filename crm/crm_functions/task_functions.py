from .api_handling import make_get_request

# Function to get tasks
def get_tasks():
    """
    Fetches all tasks from the Capsule API.

    return: JSON object containing the list of tasks.
    """
    return make_get_request('tasks')

def get_task_by_id(task_id):
    """
    Fetches a specific task by its Capsule CRM ID.

    :param task_id: The ID of the task.
    :return: The task's details as a dictionary, or None if not found.
    """
    return make_get_request(f'tasks/{task_id}')