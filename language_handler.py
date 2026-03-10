import streamlit as st
from groq import Groq
import json

class LanguageHandler:
    """
    A class to handle multilingual capabilities for the TalentScout chatbot.
    Provides language detection and translation services.
    """
    
    def __init__(self, api_key):
        """
        Initialize the LanguageHandler with the API key
        
        Args:
            api_key (str): GROQ API KEY
        """
        self.api_key = api_key
        self.client = Groq(api_key=api_key)
        self.supported_languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "zh": "Chinese",
            "hi": "Hindi",
            "ar": "Arabic",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese"
        }
        
        # Initialize language preferences
        if 'detected_language' not in st.session_state:
            st.session_state.detected_language = "en"
            
        if 'preferred_language' not in st.session_state:
            st.session_state.preferred_language = "en"
    
    def detect_language(self, text):
        """
        Detect the language of the provided text
        
        Args:
            text (str): The text to analyze
            
        Returns:
            str: The detected language code (ISO 639-1)
        """
        if not text.strip():
            return "en"  # Default to English for empty text
            
        prompt = f"""
        Analyze the following text and determine which language it is written in.
        Return ONLY the ISO 639-1 language code (e.g., 'en' for English, 'es' for Spanish).
        
        Text: "{text}"
        
        Language code:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=20
            )
            
            # Extract the language code from the response
            language_code = response.choices[0].message.content.strip().lower()
            
            # Clean up the response to ensure it's just a language code
            language_code = language_code.replace("'", "").replace('"', "")
            language_code = language_code.split()[0] if " " in language_code else language_code
            
            # Validate the language code
            if language_code in self.supported_languages:
                return language_code
            else:
                return "en"  # Default to English if unsupported
                
        except Exception:
            return "en"  # Default to English on error
    
    def translate_text(self, text, target_language="en"):
        """
        Translate text to the target language
        
        Args:
            text (str): The text to translate
            target_language (str): The target language code (ISO 639-1)
            
        Returns:
            str: The translated text
        """
        if not text.strip():
            return text
            
        # Skip translation if already in target language
        source_language = st.session_state.detected_language
        if source_language == target_language:
            return text
            
        source_lang_name = self.supported_languages.get(source_language, "Unknown")
        target_lang_name = self.supported_languages.get(target_language, "English")
        
        prompt = f"""
        Translate the following text from {source_lang_name} to {target_lang_name}.
        Preserve formatting, maintain the original meaning, and ensure the translation sounds natural.
        
        Text to translate: "{text}"
        
        Translation:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            # Remove quotes if the model included them
            if translated_text.startswith('"') and translated_text.endswith('"'):
                translated_text = translated_text[1:-1]
                
            return translated_text
            
        except Exception:
            # Return original text on error
            return text
    
    def translate_messages(self, messages, target_language):
        """
        Translate a list of chat messages to the target language
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content'
            target_language (str): The target language code
            
        Returns:
            list: The translated messages
        """
        translated_messages = []
        
        for message in messages:
            if message.get("role") == "assistant":
                # Translate assistant messages to user's preferred language
                translated_content = self.translate_text(
                    message.get("content", ""), 
                    target_language
                )
                translated_messages.append({
                    "role": message.get("role", ""),
                    "content": translated_content
                })
            else:
                # Keep user messages in their original language
                translated_messages.append(message)
                
        return translated_messages
            
    def translate_json_response(self, json_string, target_language):
        """
        Translate the 'response' field in a JSON string to the target language
        
        Args:
            json_string (str): The JSON string with a 'response' field
            target_language (str): The target language code
            
        Returns:
            str: JSON string with translated 'response' field
        """
        try:
            data = json.loads(json_string)
            
            # Only translate the response field
            if "response" in data and isinstance(data["response"], str):
                data["response"] = self.translate_text(data["response"], target_language)
                
            return json.dumps(data)
            
        except json.JSONDecodeError:
            # Return the original string if it's not valid JSON
            return json_string
    
    def get_welcome_message(self, language_code="en"):
        """
        Get a welcome message in the specified language
        
        Args:
            language_code (str): The language code
            
        Returns:
            str: Welcome message in the specified language
        """
        welcome_messages = {
            "en": "👋 Hello! I'm the TalentScout Hiring Assistant. I'll help gather some information about your profile and ask a few technical questions to match you with the right opportunities. Let's start with your full name.",
            "es": "👋 ¡Hola! Soy el Asistente de Contratación de TalentScout. Te ayudaré a recopilar información sobre tu perfil y te haré algunas preguntas técnicas para encontrar las oportunidades adecuadas. Comencemos con tu nombre completo.",
            "fr": "👋 Bonjour! Je suis l'Assistant de Recrutement TalentScout. Je vais vous aider à recueillir des informations sur votre profil et vous poser quelques questions techniques pour vous associer aux bonnes opportunités. Commençons par votre nom complet.",
            "de": "👋 Hallo! Ich bin der TalentScout Einstellungsassistent. Ich helfe Ihnen dabei, Informationen über Ihr Profil zu sammeln und stelle einige technische Fragen, um Sie mit den richtigen Möglichkeiten zu verbinden. Beginnen wir mit Ihrem vollständigen Namen.",
            "zh": "👋 你好！我是 TalentScout 招聘助手。我将帮助收集关于您个人资料的信息，并根据您的技术栈提出一些技术问题，以匹配合适的工作机会。让我们从您的全名开始。",
            "hi": "👋 नमस्ते! मैं TalentScout हायरिंग असिस्टेंट हूं। मैं आपके प्रोफ़ाइल के बारे में कुछ जानकारी इकट्ठा करने और आपको सही अवसरों से जोड़ने के लिए कुछ तकनीकी प्रश्न पूछने में मदद करूंगा। आइए आपके पूरे नाम से शुरू करें।",
            "ar": "👋 مرحباً! أنا مساعد التوظيف في TalentScout. سأساعدك في جمع بعض المعلومات حول ملفك الشخصي وطرح بعض الأسئلة التقنية لمطابقتك مع الفرص المناسبة. لنبدأ باسمك الكامل.",
            "pt": "👋 Olá! Sou o Assistente de Contratação da TalentScout. Vou ajudar a coletar algumas informações sobre seu perfil e fazer algumas perguntas técnicas para combinar você com as oportunidades certas. Vamos começar com seu nome completo.",
            "ru": "👋 Здравствуйте! Я ассистент по найму TalentScout. Я помогу собрать информацию о вашем профиле и задам несколько технических вопросов, чтобы подобрать подходящие возможности. Давайте начнем с вашего полного имени.",
            "ja": "👋 こんにちは！TalentScoutの採用アシスタントです。あなたのプロフィールに関する情報を収集し、技術的な質問をいくつか行って、適切な機会とマッチングするお手伝いをします。まず、あなたのフルネームから始めましょう。"
        }
        
        return welcome_messages.get(language_code, welcome_messages["en"])
    
    def create_language_selector(self):
        """
        Create a language selector widget for the Streamlit UI
        
        Returns:
            str: Selected language code
        """
        # Convert language codes and names to list of tuples for selectbox
        language_options = [(code, name) for code, name in self.supported_languages.items()]
        
        # Default to detected language if available
        default_index = 0
        for i, (code, _) in enumerate(language_options):
            if code == st.session_state.preferred_language:
                default_index = i
                break
        
        # Create the selector with language name as display option
        selected_option = st.sidebar.selectbox(
            "Choose Language / Elegir idioma / Choisir la langue",
            options=language_options,
            format_func=lambda x: x[1],  # Display the language name
            index=default_index
        )
        
        # Update session state with selected language
        selected_code = selected_option[0]
        st.session_state.preferred_language = selected_code
        
        return selected_code