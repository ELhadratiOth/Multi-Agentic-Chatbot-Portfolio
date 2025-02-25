def get_last_6_memories(memories):
    """
    Extracts the last 6 memory messages from a list of memory dictionaries
    and returns them as a readable string.

    :param memories: List of dictionaries containing memory information.
    :return: Formatted string of the last 6 memory messages.
    """
    print(memories)
    last_6_memories = memories[-6:]

    last_6_messages = [memory['memory'] for memory in last_6_memories]

    return "the User is asking about : "+ ". ".join(last_6_messages) + "." if last_6_messages else "No memories found."





# Example usage
memories = [
    {'id': '77a8abad-706e-4511-a8f8-3c94f5793aaf', 'memory': 'Is allergic to nuts', 'user_id': 'alex', 'metadata': None, 'categories': None, 'created_at': '2025-02-19T14:55:30.844710-08:00', 'updated_at': '2025-02-19T14:55:30.844721-08:00'},
    {'id': '7d58fa75-4256-437b-afd3-33edcb126d61', 'memory': 'Is a vegetarian', 'user_id': 'alex', 'metadata': None, 'categories': None, 'created_at': '2025-02-19T14:55:30.822851-08:00', 'updated_at': '2025-02-19T14:55:30.822861-08:00'},
    {'id': '48cf35e2-422e-4fb6-8f60-a87686309488', 'memory': 'Name is Alex', 'user_id': 'alex', 'metadata': None, 'categories': None, 'created_at': '2025-02-19T14:55:30.793452-08:00', 'updated_at': '2025-02-19T14:55:30.793464-08:00'}
]

last_3_messages = get_last_6_memories(memories)
print(last_3_messages)