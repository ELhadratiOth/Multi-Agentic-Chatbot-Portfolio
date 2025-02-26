def get_first_10_memories(memories):
    """
    Get the first 10 memories from the chat history.
    
    :param memories: Dictionary containing memory results from mem0 API
    :return: Formatted string of the first 10 memory messages, or an error message if none are found.
    """
    if not memories or 'results' not in memories:
        return "No memories found."
        
    memory_list = memories['results']
    
    # Take the first 10 elements (or all if less than 10)
    first_10_memories = memory_list[:4]
    
    try:
        first_10_messages = [memory['memory'] for memory in first_10_memories]
        return "Previous chat context: " + ". ".join(first_10_messages) + "." if first_10_messages else "No memories found."
    except Exception as e:
        print(f"Error processing memories: {e}")
        return "No memories found."