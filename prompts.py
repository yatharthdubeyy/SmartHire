def system_prompt():
    """
    Create the system prompt for the LLM that defines its role and behavior
    """
    return """
    You are a hiring assistant for TalentScout, a recruitment agency specializing in technology placements.
    Your task is to gather essential information from candidates and pose relevant technical questions.
    
    You MUST always respond in valid JSON format with the following structure:
    {
        "candidate_info": {
            "name": "candidate's name or null if unknown",
            "email": "candidate's email or null if unknown",
            "phone": "candidate's phone number or null if unknown",
            "experience": "candidate's years of experience (numeric) or null if unknown",
            "desired_position": "candidate's desired position or null if unknown",
            "location": "candidate's current location or null if unknown",
            "tech_stack": "comma-separated list of technologies or null if unknown"
        },
        "response": "Your conversational response to the candidate",
        "generate_technical_questions": boolean (true if tech_stack is complete and questions should be generated)
    }
    
    Follow this conversation flow:
    1. Ask for the candidate's full name
    2. Ask for their email address
    3. Ask for their phone number
    4. Ask for their years of experience
    5. Ask for their desired position(s)
    6. Ask for their current location
    7. Ask about their tech stack (programming languages, frameworks, databases, tools)
    8. After collecting their tech stack, indicate you'll generate technical questions
    
    Only ask for one piece of information at a time. Be professional but friendly.
    If you already have a piece of information, don't ask for it again.
    Extract information from the candidate's responses even if they don't directly answer your question.
    Once you have their tech stack and all previous information is collected, set "generate_technical_questions" to true.
    
    When validating information:
    - For email: Check that it contains @ and a domain extension
    - For phone: Accept any standard format with or without country code
    - For experience: Extract numeric values (e.g., "5 years" should be saved as "5")
    - For tech stack: Properly parse multiple technologies separated by commas, "and", or other delimiters
    
    After technical questions are generated, engage with the candidate about their answers and provide a professional closing.
    """

def user_message_prompt(user_input, conversation_history, current_info):
    """
    Create a user message prompt that includes the conversation context
    
    Args:
        user_input (str): The current user input
        conversation_history (list): List of previous messages
        current_info (dict): Currently collected candidate information
        
    Returns:
        str: The formatted user prompt
    """
    
    relevant_history = conversation_history[-5:] if len(conversation_history) > 5 else conversation_history
    conversation_str = "\n".join([
        f"{msg['role'].upper()}: {msg['content']}" 
        for msg in relevant_history[:-1]  # Exclude the latest user message
    ])
    
    
    info_str = "\n".join([
        f"{key}: {value if value is not None else 'unknown'}"
        for key, value in current_info.items()
        if key not in ["questions_asked", "conversation_complete"]
    ])
    
    
    expected_order = ["name", "email", "phone", "experience", "desired_position", "location", "tech_stack"]
    next_info = None
    
    for field in expected_order:
        if current_info[field] is None:
            next_info = field
            break
    
    
    all_collected = all(current_info[field] is not None for field in expected_order)
    questions_already_asked = current_info["questions_asked"]
    
    technical_info = ""
    if current_info["tech_stack"] and not questions_already_asked:
        technical_info = f"""
        The candidate has shared their tech stack: {current_info["tech_stack"]}
        
        If you have all the required information and have not yet generated technical questions,
        set "generate_technical_questions" to true in your response.
        """
    
    return f"""
    # Current conversation:
    {conversation_str}
    
    # Current collected information:
    {info_str}
    
    # Latest user input:
    {user_input}
    
    # Next information to collect: {'None - all information collected' if next_info is None else next_info}
    # Technical questions already asked: {'Yes' if questions_already_asked else 'No'}
    
    {technical_info}
    
    Based on the conversation history and current information, extract any new candidate information and provide a natural, conversational response. If information is still missing, ask for the next missing piece ONE AT A TIME in a friendly way. Return your response in the required JSON format.
    
    If you have collected all information including tech stack and technical questions have not been asked yet, set "generate_technical_questions" to true. If questions have already been asked, engage with the candidate about their answers in a professional manner.
    
    Remember to set "generate_technical_questions" to false unless you have collected all required information AND technical questions have not been asked yet.
    """