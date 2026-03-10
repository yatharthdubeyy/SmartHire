import streamlit as st
from groq_helper import chat_with_groq
from prompts import system_prompt, user_message_prompt
import json
import time
from collections import OrderedDict

# Import modules
from data_handler import DataHandler
from language_handler import LanguageHandler
from performance_optimizer import PerformanceOptimizer
from ui_enhancer import UIEnhancer
from sentiment_analyzer import SentimentAnalyzer  


st.set_page_config(
    page_title="TalentScout Hiring Assistant", 
    page_icon="🧑‍💻", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'ui_enhancer' not in st.session_state:
    st.session_state.ui_enhancer = UIEnhancer()
    
if 'performance_optimizer' not in st.session_state:
    st.session_state.performance_optimizer = PerformanceOptimizer(cache_size=100)
    
if 'data_handler' not in st.session_state:
    st.session_state.data_handler = DataHandler()
    
if 'language_handler' not in st.session_state:
    st.session_state.language_handler = None  # Will be initialized after API key is available
    
if 'sentiment_analyzer' not in st.session_state:
    st.session_state.sentiment_analyzer = None  
    
if 'candidate_info' not in st.session_state:
    st.session_state.candidate_info = {
        "name": None,
        "email": None,
        "phone": None,
        "experience": None,
        "desired_position": None,
        "location": None,
        "tech_stack": None,
        "questions_asked": False,
        "conversation_complete": False
    }
    
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
if 'detected_language' not in st.session_state:
    st.session_state.detected_language = "en"
    
if 'current_sentiment' not in st.session_state:
    st.session_state.current_sentiment = {}
    
if 'last_saved' not in st.session_state:
    st.session_state.last_saved = False

# Apply custom CSS styles
st.session_state.ui_enhancer.apply_custom_css()

# Start performance timing for page load
page_load_start = time.time()

# Create a main container for the entire app
main_container = st.container()

with main_container:
    st.session_state.ui_enhancer.display_logo()

    st.session_state.ui_enhancer.create_welcome_header()

# Get API key
api_key = st.secrets.get("GROQ_API_KEY", None)
if not api_key:
    with st.form("api_key_form"):
        api_key = st.text_input("Please enter your GROQ API key:", type="password")
        submit_button = st.form_submit_button("Submit")
        
        if submit_button and not api_key:
            st.error("Please provide a GROQ API key to continue.")
            st.stop()
        elif not submit_button:
            st.info("This app requires a GROQ API key to function. Please enter your key above.")
            st.stop()

# Initialize language handler for multilingual support
if st.session_state.language_handler is None:
    st.session_state.language_handler = LanguageHandler(api_key)

# Initialize sentiment analyzer
if st.session_state.sentiment_analyzer is None:
    st.session_state.sentiment_analyzer = SentimentAnalyzer(api_key)

# Create a sidebar container for better organization
with st.sidebar:
    # Create language selector in sidebar with improved styling
    st.markdown("### 🌐 Language Settings")
    selected_language = st.session_state.language_handler.create_language_selector()
    
    st.markdown("---")
    
    # Display progress tracker in sidebar
    st.markdown("### 📊 Application Progress")
    st.session_state.ui_enhancer.create_progress_tracker(st.session_state.candidate_info)
    
    st.markdown("---")
    
    # Display privacy notice in sidebar
    st.markdown("### 🔒 Privacy")
    st.session_state.ui_enhancer.display_privacy_notice()

# Initialize messages with translated welcome message if needed
if not st.session_state.messages:
    welcome_message = st.session_state.language_handler.get_welcome_message(selected_language)
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    
    # Display GDPR consent text when starting a new conversation
    gdpr_consent = st.session_state.data_handler.get_gdpr_consent_text()
    st.session_state.messages.append({"role": "assistant", "content": gdpr_consent})
    
    # Add an information card about the hiring process
    st.session_state.ui_enhancer.create_info_card(
        "How This Works", 
        "I'll ask you a few questions about your skills and experience to help match you with the right opportunities. Your data will be handled securely and in compliance with privacy regulations.",
        "🔍"
    )

# Add sentiment analysis summary in sidebar if conversation has progressed
if len(st.session_state.messages) > 3:
    with st.sidebar:
        st.markdown("### 🎭 Candidate Sentiment")
        if hasattr(st.session_state, 'sentiment_analyzer') and hasattr(st.session_state.sentiment_analyzer, 'sentiment_history') and st.session_state.sentiment_analyzer.sentiment_history:
            sentiment_trend = st.session_state.sentiment_analyzer.get_sentiment_trend()
            trend_color = st.session_state.sentiment_analyzer.get_sentiment_color(sentiment_trend["trend"])
            trend_emoji = st.session_state.sentiment_analyzer.get_sentiment_emoji(sentiment_trend["trend"])
            
            st.markdown(f"""
            <div style="padding: 15px; border: 1px solid {trend_color}; border-radius: 12px; margin-bottom: 15px; background-color: {st.session_state.ui_enhancer.dark_card}; box-shadow: 0 3px 12px rgba(0,0,0,0.2);">
                <h4 style="margin: 0 0 10px 0; color: {trend_color}; font-weight: 600;">{trend_emoji} Overall Sentiment</h4>
                <p style="margin: 0 0 5px 0;"><strong>Trend:</strong> {sentiment_trend["trend"].replace('_', ' ').title()}</p>
                <p style="margin: 0 0 5px 0;"><strong>Score:</strong> {sentiment_trend["average_score"]:.2f}</p>
                <p style="margin: 0;"><strong>Top emotions:</strong> {', '.join(sentiment_trend["top_emotions"])}</p>
            </div>
            """, unsafe_allow_html=True)

# Create a custom CSS to fix the chat layout
st.markdown("""
<style>
    /* Fix for chat layout */
    .stChatMessage {
        margin-bottom: 1rem;
    }
    
    /* Ensure the chat input stays at the bottom */
    .stChatInput {
        position: sticky;
        bottom: 0;
        background-color: #0E1117;
        padding: 1rem 0;
        z-index: 100;
    }
    
    /* Add some padding to the bottom of the chat container */
    .main .block-container {
        padding-bottom: 5rem;
    }
    
    /* Improve chat message styling */
    [data-testid="stChatMessageUser"] {
        background-color: rgba(124, 58, 237, 0.1);
        border-radius: 15px;
        padding: 10px 15px;
        margin-left: 20%;
    }
    
    [data-testid="stChatMessageAssistant"] {
        background-color: rgba(6, 182, 212, 0.1);
        border-radius: 15px;
        padding: 10px 15px;
        margin-right: 20%;
    }
</style>
""", unsafe_allow_html=True)

# Display all messages in the chat container
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Only translate assistant messages if needed
        if message["role"] == "assistant" and selected_language != st.session_state.detected_language:
            translated_content = st.session_state.language_handler.translate_text(
                message["content"], 
                selected_language
            )
            st.markdown(translated_content)
        else:
            st.markdown(message["content"])

user_input = st.chat_input("Type your response here...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Detect language of user input
    detected_language = st.session_state.language_handler.detect_language(user_input)
    st.session_state.detected_language = detected_language
    
    # Analyze sentiment of user input
    sentiment_data = st.session_state.sentiment_analyzer.analyze_sentiment(user_input)
    
    # Get suggestions based on sentiment (for internal use)
    response_suggestion = st.session_state.sentiment_analyzer.get_tailored_response_suggestion(sentiment_data)
    
    # Store sentiment data for this message
    st.session_state.current_sentiment = sentiment_data
    
    # Display visual sentiment indicator in sidebar only
    if sentiment_data and "sentiment" in sentiment_data:
        with st.sidebar:
            st.markdown("### 🎭 Current Sentiment")
            sentiment_html = st.session_state.ui_enhancer.create_sentiment_indicator(sentiment_data)
            st.markdown(sentiment_html, unsafe_allow_html=True)
    
    if any(word in user_input.lower() for word in ['bye', 'goodbye', 'exit', 'quit', 'end']):
        # Add farewell message to session state
        farewell_message = "Thank you for chatting with TalentScout's Hiring Assistant! Your information has been saved. Our recruitment team will review your profile and get back to you soon. Have a great day! 👋"
        
        # Translate farewell message if needed
        if selected_language != "en":
            farewell_message = st.session_state.language_handler.translate_text(farewell_message, selected_language)
        
        with st.chat_message("assistant"):
            st.markdown(farewell_message)
            
        st.session_state.messages.append({"role": "assistant", "content": farewell_message})
        st.session_state.candidate_info["conversation_complete"] = True
        
        # Save candidate data when conversation ends
        if st.session_state.candidate_info.get("name") or st.session_state.candidate_info.get("email"):
            st.session_state.data_handler.save_candidate_data(
                st.session_state.candidate_info,
                st.session_state.messages
            )
            
        # Show data privacy information
        with st.expander("Data Privacy Information"):
            st.markdown(st.session_state.data_handler.get_data_deletion_info())
            
        # Add footer from UIEnhancer (new integration)
        st.session_state.ui_enhancer.create_footer()
            
        st.stop()
    
    conversation_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    
    # Enhance the prompt with sentiment information
    prompt = user_message_prompt(user_input, conversation_history, st.session_state.candidate_info)
    
    # Add sentiment info to the prompt
    sentiment_info = f"""
    Recent candidate sentiment: {sentiment_data.get('sentiment', 'neutral')}
    Detected emotions: {', '.join(sentiment_data.get('emotions', ['none']))}
    Suggestion: {response_suggestion}
    """
    enhanced_prompt = prompt + "\n\n" + sentiment_info
    
    optimized_prompt = st.session_state.performance_optimizer.preprocess_prompt(enhanced_prompt)
    
    # Show typing animation while waiting for response
    with st.chat_message("assistant"):
        typing_indicator = st.session_state.ui_enhancer.display_typing_animation()
        
        with st.spinner("Thinking..."):
            # Apply caching decorator to the API call
            cached_chat_with_groq = st.session_state.performance_optimizer.cache_api_response(chat_with_groq)
            
            rate_limited_chat = PerformanceOptimizer.rate_limit(cached_chat_with_groq)
            
            # Track response time
            response_start = time.time()
            response = rate_limited_chat(api_key, system_prompt(), optimized_prompt)
            response_time = time.time() - response_start
            
            # Record the response time
            st.session_state.performance_optimizer.record_response_time(response_time)
            
            # Translate JSON response if needed
            if selected_language != "en":
                response = st.session_state.language_handler.translate_json_response(response, selected_language)
            
            try:
                parsed_response = st.session_state.performance_optimizer.optimize_json_parse(response)
                
                if "error" in parsed_response:
                    st.error(f"Error parsing response: {parsed_response['error']}")
                    fallback_message = "I apologize for the technical issue. Could you please repeat your last answer?"
                    st.markdown(fallback_message)
                    st.session_state.messages.append({"role": "assistant", "content": fallback_message})
                    
                for key, value in parsed_response["candidate_info"].items():
                    if value and value != "unknown" and value != "null":
                        st.session_state.candidate_info[key] = value
                
                st.markdown(parsed_response["response"])
                st.session_state.messages.append({"role": "assistant", "content": parsed_response["response"]})
                
                st.session_state.ui_enhancer.create_progress_tracker(st.session_state.candidate_info)
                
                milestone_messages = {
                    "name": ("Personal Info Captured", "Great! I've got your basic information. Let's continue with some more details.", "👤"),
                    "tech_stack": ("Tech Stack Identified", "Thanks for sharing your technical expertise. This helps us match you with relevant positions.", "💻"),
                    "experience": ("Experience Noted", "Your experience level has been recorded. This will help us find the right seniority level.", "📈"),
                    "location": ("Location Preferences Saved", "I've noted your location preferences. This helps us find opportunities in your area.", "📍")
                }
                
                for key, (title, message, icon) in milestone_messages.items():
                    if key in parsed_response["candidate_info"] and parsed_response["candidate_info"][key] and key in st.session_state.candidate_info:
                        if parsed_response["candidate_info"][key] == st.session_state.candidate_info[key]:
                            # Display milestone info in sidebar instead of chat
                            with st.sidebar:
                                st.session_state.ui_enhancer.create_info_card(title, message, icon)
                
                if parsed_response.get("generate_technical_questions", False) and not st.session_state.candidate_info["questions_asked"]:
                    tech_stack = st.session_state.candidate_info["tech_stack"]
                    
                    if tech_stack:
                        # Create an info card for the technical questions section
                        st.session_state.ui_enhancer.create_info_card(
                            "Technical Assessment", 
                            "Please answer the following questions to help us evaluate your technical expertise.",
                            "💻"
                        )
                        
                        with st.spinner("Generating technical questions..."):
                            tech_questions_prompt = f"""
                            Generate 3-5 technical interview questions to assess a candidate's knowledge in the following technologies:
                            {tech_stack}

                            Focus on core concepts, practical applications, and some advanced topics appropriate for their {st.session_state.candidate_info['experience']} years of experience.
                            Format your response as a JSON object with a single 'questions' field containing an array of question strings.
                            Do NOT include any numbering in the questions themselves.
                            Example format:
                            {{
                                "questions": [
                                    "Explain the difference between a list and a tuple in Python.",
                                    "How would you optimize a slow SQL query?",
                                    "Describe the benefits of containerization with Docker."
                                ]
                            }}
                            """

                            optimized_tech_prompt = st.session_state.performance_optimizer.preprocess_prompt(tech_questions_prompt)
                            
                            cached_chat = st.session_state.performance_optimizer.cache_api_response(chat_with_groq)
                            rate_limited_chat = PerformanceOptimizer.rate_limit(cached_chat)
                            
                            response_start = time.time()
                            questions_response = rate_limited_chat(api_key, "", optimized_tech_prompt)
                            response_time = time.time() - response_start
                            
                            st.session_state.performance_optimizer.record_response_time(response_time)
                            
                            # Translate technical questions if needed
                            if selected_language != "en":
                                try:
                                    questions_data = json.loads(questions_response)
                                    if isinstance(questions_data.get('questions'), list):
                                        translated_questions = []
                                        for question in questions_data['questions']:
                                            translated_question = st.session_state.language_handler.translate_text(
                                                question, selected_language
                                            )
                                            translated_questions.append(translated_question)
                                        questions_data['questions'] = translated_questions
                                        questions_response = json.dumps(questions_data)
                                except json.JSONDecodeError:
                                    questions_response = st.session_state.language_handler.translate_text(
                                        questions_response, selected_language
                                    )

                            try:
                                questions_data = json.loads(questions_response)
                                if isinstance(questions_data.get('questions'), list):
                                    formatted_questions = ""
                                    for i, question in enumerate(questions_data['questions']):
                                        clean_question = question.strip()
                                        
                                        if clean_question[0].isdigit() and '.' in clean_question[:3]:
                                            clean_question = clean_question.split('.', 1)[1].strip()
                                        formatted_questions += f"{i+1}. {clean_question}\n\n"
                                else:
                                    formatted_questions = questions_response
                            except json.JSONDecodeError:
                                lines = questions_response.strip().split('\n')
                                formatted_questions = ""
                                for i, line in enumerate(lines):
                                    if line.strip():
                                        clean_line = line.strip()
                                        if clean_line[0].isdigit() and '.' in clean_line[:3]:
                                            clean_line = clean_line.split('.', 1)[1].strip()
                                        formatted_questions += f"{i+1}. {clean_line}\n\n"

                            # Translate the header for technical questions if needed
                            technical_questions_header = "### Based on your tech stack, here are some technical questions:"
                            if selected_language != "en":
                                technical_questions_header = st.session_state.language_handler.translate_text(
                                    technical_questions_header, selected_language
                                )

                            # Add a styled card for technical questions (new integration)
                            st.session_state.ui_enhancer.create_info_card(
                                "Technical Assessment Started",
                                "We're now moving into the technical assessment phase. Please answer each question to showcase your expertise.",
                                "🧠"
                            )

                            questions_message = f"{technical_questions_header}\n\n{formatted_questions}"
                            st.markdown(questions_message)

                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": questions_message
                            })
                            
                            st.session_state.candidate_info["questions_asked"] = True
                            
                            # Translate follow-up message if needed
                            follow_up = "Please provide your answers to these questions. This will help us better understand your technical expertise."
                            if selected_language != "en":
                                follow_up = st.session_state.language_handler.translate_text(
                                    follow_up, selected_language
                                )
                                
                            st.markdown(follow_up)
                            st.session_state.messages[-1]["content"] += "\n\n" + follow_up

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                fallback_message = "I apologize for the technical issue. Could you please repeat your last answer?"
                st.markdown(fallback_message)
                st.session_state.messages.append({"role": "assistant", "content": fallback_message})

# Save data periodically if significant information is collected
if (st.session_state.candidate_info.get("name") and 
    st.session_state.candidate_info.get("email") and 
    not st.session_state.candidate_info.get("conversation_complete", False)):
    # Save candidate data in session for recovery purposes
    if not st.session_state.last_saved:
        st.session_state.data_handler.save_candidate_data(
            st.session_state.candidate_info,
            st.session_state.messages
        )
        st.session_state.last_saved = True

# Calculate and display performance metrics in the sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📈 Performance Metrics")
    
    # Calculate page load time
    page_load_time = time.time() - page_load_start
    
    # Get average response time
    avg_response_time = st.session_state.performance_optimizer.get_average_response_time()
    
    # Display metrics in a styled card
    st.markdown(f"""
    <div style="padding: 15px; border-radius: 12px; background-color: {st.session_state.ui_enhancer.dark_card}; box-shadow: 0 3px 12px rgba(0,0,0,0.2);">
        <p style="margin: 0 0 5px 0;"><strong>Page Load Time:</strong> {page_load_time:.2f}s</p>
        <p style="margin: 0 0 5px 0;"><strong>Avg Response Time:</strong> {avg_response_time:.2f}s</p>
        <p style="margin: 0;"><strong>Cache Hits:</strong> {st.session_state.performance_optimizer.cache_hits}</p>
    </div>
    """, unsafe_allow_html=True)

# Add sentiment analysis admin view
with st.sidebar.expander("Sentiment Analysis", expanded=False):
    st.markdown("### Candidate Sentiment Analytics")
    if hasattr(st.session_state, 'sentiment_analyzer') and hasattr(st.session_state.sentiment_analyzer, 'sentiment_history') and st.session_state.sentiment_analyzer.sentiment_history:
        sentiment_trend = st.session_state.sentiment_analyzer.get_sentiment_trend()
        st.markdown(f"**Overall Trend:** {sentiment_trend['trend'].replace('_', ' ').title()}")
        st.markdown(f"**Average Score:** {sentiment_trend['average_score']:.2f}")
        st.markdown(f"**Top Emotions:** {', '.join(sentiment_trend['top_emotions'])}")
        
        # Display last few sentiment analyses
        st.markdown("### Recent Sentiment Analysis")
        for i, entry in enumerate(st.session_state.sentiment_analyzer.sentiment_history[-3:]):
            analysis = entry.get("analysis", {})
            text = entry.get("text", "")
            if len(text) > 50:
                text = text[:50] + "..."
                
            sentiment = analysis.get("sentiment", "neutral")
            score = analysis.get("score", 0)
            emotions = analysis.get("emotions", [])
            
            emoji = st.session_state.sentiment_analyzer.get_sentiment_emoji(sentiment)
            st.markdown(f"**Entry {len(st.session_state.sentiment_analyzer.sentiment_history) - 3 + i + 1}:** {emoji} {sentiment.replace('_', ' ').title()} ({score:.2f})")
            st.markdown(f"*Emotions:* {', '.join(emotions)}")
            st.markdown(f"*Text:* '{text}'")
            st.markdown("---")
    else:
        st.markdown("No sentiment data available yet.")

# Displaying the current collected information (for debugging)
if st.sidebar.checkbox("Show collected candidate information", False):
    # Show the original and anonymized data
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        st.write("Original Data:")
        st.json(st.session_state.candidate_info)
    
    with col2:
        st.write("Anonymized Data:")
        anonymized_data = st.session_state.data_handler.anonymize_data(st.session_state.candidate_info)
        st.json(anonymized_data)

# Data Management Tools (for admin access)
with st.sidebar.expander("Admin Tools", expanded=False):
    st.info("These tools are intended for administrators only.")
    
    if st.button("Generate Test Candidates"):
        test_candidates = st.session_state.data_handler.generate_simulated_candidates(5)
        for candidate in test_candidates:
            st.session_state.data_handler.save_candidate_data(candidate)
        st.success(f"Created {len(test_candidates)} test candidates")
    
    # Add Sentiment Reset Button
    if st.button("Reset Sentiment Analysis"):
        st.session_state.sentiment_analyzer = SentimentAnalyzer(api_key)
        st.success("Sentiment analysis reset successfully")
        
    # Performance controls
    st.markdown("### Performance Controls")
    
    # Clear cache button
    if st.button("Clear Response Cache"):
        st.session_state.performance_optimizer.cache = OrderedDict()
        st.session_state.performance_optimizer.cache_hits = 0
        st.session_state.performance_optimizer.cache_misses = 0
        st.session_state.performance_stats['cache_hits'] = 0
        st.session_state.performance_stats['cache_misses'] = 0
        st.success("Cache cleared successfully")
        
    # Reset performance stats
    if st.button("Reset Performance Stats"):
        st.session_state.performance_stats = {
            'api_calls': 0,
            'avg_response_time': 0,
            'cache_hits': 0, 
            'cache_misses': 0
        }
        st.session_state.performance_optimizer.response_times = []
        st.success("Performance stats reset")


st.session_state.ui_enhancer.create_footer()