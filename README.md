# 🤖 AI Hiring Assistant

## Overview
AI Hiring Assistant is an intelligent conversational chatbot designed to streamline the **initial screening process** for a technology recruitment agency. The system interacts with candidates through a conversational interface, collects important candidate information, and generates customized technical questions based on the candidate’s declared technology stack.

The goal of this project is to simplify early-stage recruitment by automating candidate interaction while providing recruiters with structured and meaningful insights about applicants.

---

# 🚀 Key Features

## Interactive User Interface
The application provides a modern and intuitive interface built using Streamlit, enabling seamless interaction between candidates and the chatbot.

Main interface capabilities include:

- Clean and responsive chat interface
- Real-time conversation flow
- Typing indicators for natural interaction
- Progress tracking during candidate data collection
- Sentiment analysis visualization
- Multilingual conversation support

---
## 🔑 Groq API Key Configuration

This project requires a **Groq API key** to generate AI responses.

### Step 1: Create the Streamlit secrets file

Inside the project root, create the following folder and file:
.streamlit/secrets.toml

### Step 2: Add your Groq API key

Insert the following configuration into the file:

```toml
GROQ_API_KEY="YOUR_API_KEY"

# 💬 Chatbot Functionalities

## Candidate Information Collection
The chatbot begins with a friendly introduction and collects essential candidate details required for the screening process.

Information collected includes:

- Full Name  
- Email Address  
- Phone Number  
- Years of Experience  
- Desired Job Position(s)  
- Current Location  
- Technology Stack

This structured data helps recruiters quickly understand the candidate’s profile.

---

## Technical Question Generation
Once the candidate's technology stack is collected, the system generates technical questions tailored to the provided skills.

Key characteristics include:

- Generates **3–5 technical questions per technology**
- Questions are tailored to the candidate’s skill set
- Difficulty level adjusts according to experience level
- Questions are presented in a structured format for clarity

This enables recruiters to evaluate technical competency effectively.

---

## Context Awareness
The chatbot maintains context throughout the entire conversation.

Capabilities include:

- Tracking previously collected candidate information
- Extracting details from varied user responses
- Supporting natural, non-linear conversation flows
- Avoiding repetition of previously asked questions

---

## Conversation Management
The system manages the full conversation lifecycle.

Features include:

- Recognizing conversation-ending keywords such as *exit* or *bye*
- Handling unexpected inputs with fallback responses
- Gracefully ending conversations
- Providing a summary of next steps after the screening

---

# ⚙️ Technical Stack

## Programming Language and Libraries

The project is built using the following technologies:

- **Python** – Core application development
- **Streamlit** – Frontend user interface
- **Groq API** – Large Language Model integration
- **JSON** – Structured data storage and processing

---

# 🏗 System Architecture

The project follows a modular architecture consisting of several components.

### 1. User Interface
`app.py`

Handles:
- Streamlit UI
- Chat interaction
- Conversation flow management

---

### 2. LLM Integration
`groq_helper.py`

Responsible for:
- Communicating with the Groq API
- Sending prompts and receiving responses from the language model

---

### 3. Prompt Engineering
`prompts.py`

Defines structured prompts that guide the AI assistant behavior including:

- System role definition
- Conversation management
- Technical question generation
- Context-aware responses

---

### 4. Session Management

Streamlit session state is used to:

- Maintain conversation history
- Track collected candidate information
- Store chatbot state during the interaction

---

### 5. Enhancement Modules

Additional modules enhance system functionality:

`data_handler.py`
- Handles candidate data processing and storage

`language_handler.py`
- Enables multilingual conversation support

`performance_optimizer.py`
- Implements caching and response optimization

`ui_enhancer.py`
- Improves UI appearance and responsiveness

`sentiment_analyzer.py`
- Performs sentiment analysis during conversations

---

# 🧠 Prompt Engineering Strategy

The assistant uses structured prompt engineering techniques to maintain intelligent and consistent responses.

### System Prompt
Defines:
- Assistant role
- Conversation style
- Expected response format

### User Context Prompt
Maintains:
- Conversation history
- Current candidate data
- Information still required

### Technical Question Prompt
Generates:
- Technology-specific interview questions
- Difficulty adjustment based on experience

### Sentiment-Aware Prompting
Incorporates sentiment signals to generate empathetic and adaptive responses.

---

# 🛠 Installation Guide

## Prerequisites

- Python 3.8 or higher
- Groq API Key

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Taskmaster-1/Hiring-Assistant.git
cd Hiring-Assistant