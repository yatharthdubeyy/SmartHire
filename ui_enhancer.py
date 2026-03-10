import streamlit as st

class UIEnhancer:
    """
    A class to enhance the Streamlit UI for the TalentScout chatbot with a dark theme.
    Provides custom styling, progress indicators, and interactive elements.
    """
    
    def __init__(self):
        """Initialize the UI enhancer with dark theme styling"""
        # Define dark color scheme
        self.primary_color = "#7C3AED"  # Vibrant purple
        self.secondary_color = "#06B6D4"  # Cyan
        self.accent_color = "#F472B6"  # Pink
        self.dark_bg = "#0F172A"  # Darker blue-black
        self.dark_card = "#1E293B"  # Slate dark
        self.dark_text = "#F1F5F9"  # Light gray
        self.dark_border = "#334155"  # Slate border
        self.success_color = "#10B981"  # Emerald
        self.warning_color = "#F59E0B"  # Amber
        self.error_color = "#EF4444"  # Red
        
        # Define logo (dark theme compatible)
        self.logo_svg = """
        <svg width="250" height="60" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#7C3AED;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#06B6D4;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="250" height="60" fill="url(#grad1)" rx="12" ry="12"/>
            <text x="75" y="38" fill="white" font-family="Arial" font-weight="bold" font-size="22">TalentScout</text>
            <circle cx="35" cy="30" r="18" fill="#F472B6"/>
            <text x="35" y="36" dominant-baseline="middle" text-anchor="middle" fill="white" font-family="Arial" font-weight="bold" font-size="18">TS</text>
        </svg>
        """
        
    def apply_custom_css(self):
        """Apply custom dark theme CSS to enhance the appearance of the Streamlit app"""
        css = f"""
        <style>
            /* Main app styling */
            .stApp {{
                background-color: {self.dark_bg} !important;
                color: {self.dark_text} !important;
            }}
            
            /* Main content area styling */
            .main .block-container {{
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 800px;
                background-color: {self.dark_card};
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                margin: 0 auto;
                padding-left: 2rem;
                padding-right: 2rem;
                border: 1px solid {self.dark_border};
            }}
            
            /* Header styling */
            .stApp header {{
                background-color: transparent !important;
                border-bottom: none !important;
            }}
            
            /* Text styling */
            p, .stMarkdown, .stMarkdown p {{
                color: {self.dark_text} !important;
                line-height: 1.6 !important;
            }}
            
            /* Title styling */
            h1 {{
                color: {self.primary_color} !important;
                font-weight: 700 !important;
                font-size: 2.2rem !important;
                margin-bottom: 1rem !important;
                letter-spacing: -0.5px !important;
            }}
            
            h2 {{
                color: {self.secondary_color} !important;
                font-weight: 600 !important;
                font-size: 1.8rem !important;
                letter-spacing: -0.3px !important;
            }}
            
            h3 {{
                color: {self.dark_text} !important;
                font-weight: 500 !important;
                font-size: 1.4rem !important;
                margin-top: 1rem !important;
                letter-spacing: -0.2px !important;
            }}
            
            /* Chat message styling */
            [data-testid="stChatMessage"] {{
                border-radius: 15px !important;
                padding: 16px !important;
                margin-bottom: 15px !important;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
                border: 1px solid {self.dark_border} !important;
                background-color: {self.dark_card} !important;
                transition: all 0.3s ease !important;
            }}
            
            [data-testid="stChatMessage"]:hover {{
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
            }}
            
            /* User message styling */
            [data-testid="stChatMessageUser"] {{
                background-color: {self.primary_color}15 !important;
                border-top-right-radius: 5px !important;
                border-left: 3px solid {self.primary_color} !important;
            }}
            
            /* Assistant message styling */
            [data-testid="stChatMessageAssistant"] {{
                background-color: {self.secondary_color}10 !important;
                border-top-left-radius: 5px !important;
                border-left: 3px solid {self.secondary_color} !important;
            }}
            
            /* Input box styling */
            [data-testid="stChatInput"] {{
                background-color: {self.dark_card} !important;
                border: 1px solid {self.dark_border} !important;
                color: {self.dark_text} !important;
                border-radius: 25px !important;
                padding: 12px 20px !important;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
                transition: all 0.3s ease !important;
            }}
            
            [data-testid="stChatInput"]:focus {{
                border-color: {self.primary_color} !important;
                box-shadow: 0 0 0 2px {self.primary_color}30 !important;
            }}
            
            /* Button styling */
            button[kind="primary"] {{
                background-color: {self.primary_color} !important;
                border-radius: 20px !important;
                border: none !important;
                padding: 0.5rem 1.5rem !important;
                font-weight: 500 !important;
                transition: all 0.3s ease !important;
            }}
            
            button[kind="primary"]:hover {{
                background-color: {self.primary_color}dd !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px {self.primary_color}40 !important;
            }}
            
            /* Progress bar styling */
            .stProgress > div > div {{
                background-color: {self.secondary_color} !important;
                border-radius: 4px !important;
            }}
            
            /* Sidebar styling */
            [data-testid="stSidebar"] {{
                background-color: {self.dark_card} !important;
                border-right: 1px solid {self.dark_border} !important;
                padding-top: 1rem !important;
                color: {self.dark_text} !important;
            }}
            
            [data-testid="stSidebar"] > div:first-child {{
                padding-top: 1rem !important;
                padding-left: 1.5rem !important;
                padding-right: 1.5rem !important;
            }}
            
            [data-testid="stSidebar"] .block-container {{
                padding-top: 0 !important;
            }}
            
            /* Card styling */
            .info-card {{
                background-color: {self.dark_card};
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 3px 12px rgba(0,0,0,0.2);
                border-left: 4px solid {self.primary_color};
                animation: slideIn 0.5s ease-out forwards;
                color: {self.dark_text};
                transition: all 0.3s ease;
            }}
            
            .info-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }}
            
            @keyframes slideIn {{
                from {{ transform: translateX(-20px); opacity: 0; }}
                to {{ transform: translateX(0); opacity: 1; }}
            }}
            
            /* Progress steps styling */
            .step-container {{
                display: flex;
                justify-content: space-between;
                margin: 1.25rem 0;
                position: relative;
                padding: 0 10px;
            }}
            
            .step-container::before {{
                content: "";
                position: absolute;
                top: 15px;
                left: 25px;
                right: 25px;
                height: 3px;
                background-color: {self.dark_border};
                z-index: 0;
            }}
            
            .step {{
                width: 32px;
                height: 32px;
                border-radius: 50%;
                background-color: {self.dark_border};
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: {self.dark_text};
                z-index: 1;
                position: relative;
                transition: all 0.3s ease;
            }}
            
            .step.active {{
                background-color: {self.primary_color};
                box-shadow: 0 0 0 3px {self.primary_color}30;
                color: white;
                transform: scale(1.1);
            }}
            
            .step.complete {{
                background-color: {self.success_color};
                box-shadow: 0 0 0 3px {self.success_color}30;
                color: white;
            }}
            
            /* Tooltip styling */
            .tooltip {{
                position: relative;
                display: inline-block;
                margin: 0 5px;
            }}
            
            .tooltip .tooltiptext {{
                visibility: hidden;
                width: 120px;
                background-color: {self.dark_card};
                color: {self.dark_text};
                text-align: center;
                border-radius: 6px;
                padding: 5px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -60px;
                opacity: 0;
                transition: opacity 0.3s;
                font-size: 0.8rem;
                border: 1px solid {self.dark_border};
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            }}
            
            .tooltip:hover .tooltiptext {{
                visibility: visible;
                opacity: 1;
            }}
            
            /* Progress info styling */
            .progress-info {{
                display: flex;
                align-items: center;
                margin-bottom: 8px;
                padding: 8px;
                border-radius: 8px;
                background-color: {self.dark_bg};
                transition: all 0.3s ease;
            }}
            
            .progress-info:hover {{
                transform: translateX(5px);
                background-color: {self.dark_border};
            }}
            
            .progress-info-icon {{
                margin-right: 10px;
                font-size: 1.2rem;
            }}
            
            .progress-info-text {{
                font-size: 0.9rem;
            }}
            
            /* Typing animation */
            .typing-animation {{
                display: inline-block;
                background-color: {self.dark_card};
                padding: 12px 18px;
                border-radius: 18px;
                margin: 5px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            }}
            
            .typing-dot {{
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background-color: {self.secondary_color};
                margin-right: 4px;
                animation: typing-dot-animation 1.5s infinite ease-in-out;
            }}
            
            @keyframes typing-dot-animation {{
                0% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-8px); }}
                100% {{ transform: translateY(0); }}
            }}
            
            /* Tooltip styling */
            .tooltip .tooltiptext {{
                background-color: {self.dark_card};
                color: {self.dark_text};
                border: 1px solid {self.dark_border};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 0.9rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            }}
            
            /* Privacy notice styling */
            .privacy-notice {{
                background-color: {self.dark_card};
                border-radius: 12px;
                padding: 1.25rem;
                margin: 1rem 0;
                border-left: 4px solid {self.secondary_color};
                box-shadow: 0 3px 12px rgba(0,0,0,0.2);
            }}
            
            /* Code block styling */
            pre {{
                background-color: {self.dark_bg} !important;
                border-radius: 8px !important;
                padding: 1rem !important;
                border: 1px solid {self.dark_border} !important;
            }}
            
            code {{
                color: {self.accent_color} !important;
                background-color: {self.dark_bg} !important;
                padding: 0.2rem 0.4rem !important;
                border-radius: 4px !important;
                font-family: 'Fira Code', monospace !important;
            }}
            
            /* Selectbox styling */
            .stSelectbox > div > div {{
                background-color: {self.dark_card} !important;
                border-color: {self.dark_border} !important;
                color: {self.dark_text} !important;
                border-radius: 8px !important;
            }}
            
            /* Expander styling */
            .streamlit-expanderHeader {{
                background-color: {self.dark_card} !important;
                color: {self.dark_text} !important;
                border-radius: 8px !important;
                padding: 1rem !important;
                border: 1px solid {self.dark_border} !important;
            }}
            
            .streamlit-expanderContent {{
                background-color: {self.dark_card} !important;
                color: {self.dark_text} !important;
                border-radius: 0 0 8px 8px !important;
                padding: 1rem !important;
                border: 1px solid {self.dark_border} !important;
                border-top: none !important;
            }}
            
            /* Success message styling */
            .stAlert {{
                background-color: {self.success_color}15 !important;
                border: 1px solid {self.success_color} !important;
                color: {self.dark_text} !important;
                border-radius: 8px !important;
                padding: 1rem !important;
            }}
            
            /* Warning message styling */
            .stWarning {{
                background-color: {self.warning_color}15 !important;
                border: 1px solid {self.warning_color} !important;
                color: {self.dark_text} !important;
                border-radius: 8px !important;
                padding: 1rem !important;
            }}
            
            /* Error message styling */
            .stError {{
                background-color: {self.error_color}15 !important;
                border: 1px solid {self.error_color} !important;
                color: {self.dark_text} !important;
                border-radius: 8px !important;
                padding: 1rem !important;
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    
    def display_logo(self):
        """Display the TalentScout logo"""
        logo_html = f"""
        <div style="display: flex; justify-content: center; margin-bottom: 1.5rem; margin-top: 0.5rem;">
            {self.logo_svg}
        </div>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
    
    def create_progress_tracker(self, candidate_info):
        """
        Create a visual progress tracker for the conversation flow
        
        Args:
            candidate_info (dict): The current candidate information
        """
        fields = [
            ("name", "Name"),
            ("email", "Email"),
            ("phone", "Phone"),
            ("experience", "Experience"),
            ("desired_position", "Position"),
            ("location", "Location"),
            ("tech_stack", "Tech Stack")
        ]
        
        completed = sum(1 for field, _ in fields if candidate_info.get(field))
        progress_percentage = int((completed / len(fields)) * 100)
        
        # Display progress header
        st.sidebar.markdown(f"""
        <div class="sidebar-section">
            <h3 style="margin-top: 0; margin-bottom: 10px; color: {self.secondary_color};">Your Application Progress</h3>
            <div style="font-size: 0.9rem; margin-bottom: 0.5rem; color: {self.dark_text};">Complete the interview to submit your application</div>
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span style="font-size: 0.85rem;">Progress</span>
                <span style="font-size: 0.85rem; font-weight: bold; color: {self.secondary_color};">{progress_percentage}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display progress bar
        st.sidebar.progress(progress_percentage)
        
        # Create a container for the steps
        steps_container = st.sidebar.container()
        
        # Create columns for the steps
        cols = steps_container.columns(len(fields))
        
        # Display each step in its own column
        for i, (field, name) in enumerate(fields):
            with cols[i]:
                if candidate_info.get(field):
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="width: 32px; height: 32px; border-radius: 50%; background-color: {self.success_color}; 
                             display: flex; align-items: center; justify-content: center; margin: 0 auto; 
                             color: white; font-weight: bold; box-shadow: 0 0 0 3px {self.success_color}30;">
                            ✓
                        </div>
                        <div style="font-size: 0.8rem; margin-top: 5px; color: {self.dark_text};">
                            {name}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                elif all(candidate_info.get(f) for f, _ in fields[:i]):
                    # Active step
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="width: 32px; height: 32px; border-radius: 50%; background-color: {self.primary_color}; 
                             display: flex; align-items: center; justify-content: center; margin: 0 auto; 
                             color: white; font-weight: bold; box-shadow: 0 0 0 3px {self.primary_color}30; transform: scale(1.1);">
                            {i+1}
                        </div>
                        <div style="font-size: 0.8rem; margin-top: 5px; color: {self.dark_text};">
                            {name}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Inactive step
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="width: 32px; height: 32px; border-radius: 50%; background-color: {self.dark_border}; 
                             display: flex; align-items: center; justify-content: center; margin: 0 auto; 
                             color: {self.dark_text}; font-weight: bold;">
                            {i+1}
                        </div>
                        <div style="font-size: 0.8rem; margin-top: 5px; color: {self.dark_text};">
                            {name}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.sidebar.markdown("---")
        
        # Display collected information
        st.sidebar.markdown(f"""
        <div class="sidebar-section">
            <h3 style="margin-top: 0; margin-bottom: 15px; color: {self.secondary_color};">Information Collected</h3>
        """, unsafe_allow_html=True)
        
        for field, display_name in fields:
            value = candidate_info.get(field)
            if value:
                st.sidebar.markdown(f"""
                <div class="progress-info">
                    <div class="progress-info-icon" style="color: {self.secondary_color};">✓</div>
                    <div class="progress-info-text"><strong>{display_name}:</strong> {value}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.sidebar.markdown(f"""
                <div class="progress-info">
                    <div class="progress-info-icon" style="color: #666;">○</div>
                    <div class="progress-info-text"><strong>{display_name}:</strong> <span style="color: #666;">Not provided</span></div>
                </div>
                """, unsafe_allow_html=True)
                
        if candidate_info.get("questions_asked"):
            st.sidebar.markdown(f"""
            <div class="progress-info">
                <div class="progress-info-icon" style="color: {self.secondary_color};">✓</div>
                <div class="progress-info-text">
                    <strong>Technical Questions</strong>
                    <span style="color: {self.secondary_color}; font-size: 0.8em; margin-left: 8px;">Completed</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f"""
            <div class="progress-info">
                <div class="progress-info-icon" style="color: #666;">○</div>
                <div class="progress-info-text">
                    <strong>Technical Questions</strong>
                    <span style="color: #666; font-size: 0.8em; margin-left: 8px;">Pending</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    def display_typing_animation(self):
        """Display a typing animation while waiting for a response"""
        typing_html = """
        <div class="typing-animation">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
        """
        return st.markdown(typing_html, unsafe_allow_html=True)
    
    def display_privacy_notice(self):
        """Display a GDPR-compliant privacy notice"""
        privacy_html = f"""
        <div class="privacy-notice">
            <h4 style="margin-top: 0; color: {self.secondary_color};">📋 Privacy Notice</h4>
            <p style="font-size: 0.9rem; margin-bottom: 0.5rem;">Your personal information is being collected and processed in accordance with GDPR regulations. 
            We only collect information necessary for the recruitment process, and your data is stored securely 
            with encryption.</p>
            <p style="font-size: 0.9rem; margin-bottom: 0;">You have the right to access, correct, or request deletion of your data at any time. 
            For more information, please contact <a href="mailto:privacy@talentscout.example.com" style="color: {self.secondary_color}; text-decoration: none;">privacy@talentscout.example.com</a></p>
        </div>
        """
        st.sidebar.markdown(privacy_html, unsafe_allow_html=True)
    
    def create_info_card(self, title, content, icon="ℹ️"):
        """
        Create a styled information card
        
        Args:
            title (str): Card title
            content (str): Card content
            icon (str): Emoji icon for the card
        """
        card_html = f"""
        <div class="info-card">
            <h4 style="color: {self.primary_color}; margin-top: 0;">{icon} {title}</h4>
            <p style="margin-bottom: 0;">{content}</p>
        </div>
        """
        return st.markdown(card_html, unsafe_allow_html=True)
    
    def create_sentiment_indicator(self, sentiment_data):
        """
        Create a visual indicator for the detected sentiment
        
        Args:
            sentiment_data (dict): The sentiment analysis results
            
        Returns:
            str: HTML for the sentiment indicator
        """
        sentiment = sentiment_data.get("sentiment", "neutral")
        score = sentiment_data.get("score", 0)
        
        colors = {
            "very_positive": "#00CEC9",
            "positive": "#55E6C1",
            "neutral": "#6C5CE7",
            "negative": "#FD79A8", 
            "very_negative": "#E84393"
        }
        color = colors.get(sentiment, "#6C5CE7")
        
        emojis = {
            "very_positive": "😃",
            "positive": "🙂",
            "neutral": "😐",
            "negative": "🙁",
            "very_negative": "😞"
        }
        emoji = emojis.get(sentiment, "😐")
        
        gauge_position = int((score + 1) * 50)
        
        html = f"""
        <div class="sentiment-indicator">
            <div style="font-size: 28px; margin-bottom: 5px;">{emoji}</div>
            <div style="font-weight: bold; color: {color}; margin-bottom: 8px;">{sentiment.replace('_', ' ').title()}</div>
            <div style="background-color: #333; height: 8px; border-radius: 4px; margin: 5px 0;">
                <div style="background-color: {color}; width: {gauge_position}%; height: 100%; border-radius: 4px; transition: width 0.5s ease-in-out;"></div>
            </div>
        </div>
        """
        
        return html
    
    def create_welcome_header(self):
        """Create a visually appealing welcome header"""
        welcome_html = f"""
        <div style="text-align: center; margin: 1.5rem 0;">
            <h1 style="color: {self.primary_color}; margin-bottom: 0.5rem;">Welcome to TalentScout</h1>
            <p style="font-size: 1.1rem; color: {self.secondary_color}; margin-bottom: 1.5rem;">We connect tech talent with great opportunities</p>
            <div style="height: 4px; width: 50px; background: linear-gradient(to right, {self.primary_color}, {self.secondary_color}); margin: 0 auto;"></div>
        </div>
        """
        return st.markdown(welcome_html, unsafe_allow_html=True)
    
    def create_footer(self):
        """Create a footer for the app"""
        footer_html = f"""
        <div style="text-align: center; margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid {self.dark_border};">
            <p style="color: {self.secondary_color}; font-size: 0.85rem;">© 2025 TalentScout - AI-Powered Recruitment Assistant</p>
            <p style="color: #777; font-size: 0.75rem;">Helping match talent with dream jobs</p>
        </div>
        """
        return st.markdown(footer_html, unsafe_allow_html=True)