from groq import Groq

def chat_with_groq(api_key, system_prompt, user_prompt):
    """
    Interact with the Groq LLM API
    
    Args:
        api_key (str): The API key for Groq
        system_prompt (str): The system prompt for the LLM
        user_prompt (str): The user prompt for the LLM
        
    Returns:
        str: The LLM response content
    """
    client = Groq(api_key=api_key)
    
    messages = []
    
    wants_json = False
    if system_prompt:
        wants_json = "JSON" in system_prompt.upper()
        messages.append({"role": "system", "content": system_prompt})
    
    
    if "json" not in user_prompt.lower() and not wants_json:
        user_prompt = f"{user_prompt}\n\nProvide your response in JSON format."
    
    messages.append({"role": "user", "content": user_prompt})
    
    # Setup parameters for the API call
    params = {
        "model": "llama3-70b-8192",
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 1000
    }
    
    params["response_format"] = {"type": "json_object"}
    
    try:
        response = client.chat.completions.create(**params)
        return response.choices[0].message.content
    except Exception as e:
        return f'{{"error": "API Error: {str(e)}"}}'