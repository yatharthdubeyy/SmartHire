from groq import Groq
import re
import json
import streamlit as st

class SentimentAnalyzer:
    """
    A class to analyze the sentiment and emotional tone of candidate responses
    during the interview process.
    """
    
    def __init__(self, api_key):
        """
        Initialize the SentimentAnalyzer with the API key
        
        Args:
            api_key (str): GROQ API KEY
        """
        self.api_key = api_key
        self.client = Groq(api_key=api_key)
        self.sentiment_history = []
        
    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of a message using the LLM
        
        Args:
            text (str): The message to analyze
            
        Returns:
            dict: The sentiment analysis results
        """
        if not text.strip():
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "emotions": [],
                "confidence": 0.0
            }
            
        # Simplified prompt for sentiment analysis
        prompt = f"""
        Analyze the sentiment and emotions in the following text from a job candidate.
        Return ONLY a JSON object with the following fields:
        - sentiment: one of ["very_negative", "negative", "neutral", "positive", "very_positive"]
        - score: a number from -1.0 (very negative) to 1.0 (very positive)
        - emotions: an array of emotions detected (e.g., ["excited", "nervous", "confident"])
        - confidence: a number from 0.0 to 1.0 indicating confidence in this analysis
        
        Text to analyze: "{text}"
        
        JSON response:
        """
        
        try:
            # Call the API with a low temperature for more consistent results
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=200,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Store in history
            self.sentiment_history.append({
                "text": text,
                "analysis": result
            })
            
            return result
            
        except Exception as e:
            # Return a default neutral sentiment on error
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "emotions": ["unknown"],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def get_sentiment_trend(self):
        """
        Analyze the trend of sentiment throughout the conversation
        
        Returns:
            dict: Summary of sentiment trends
        """
        if not self.sentiment_history:
            return {"trend": "neutral", "details": "No sentiment history available"}
            
        # Calculate average sentiment score
        scores = [entry.get("analysis", {}).get("score", 0) 
                 for entry in self.sentiment_history]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Determine overall trend
        if avg_score > 0.5:
            trend = "very_positive"
        elif avg_score > 0.1:
            trend = "positive"
        elif avg_score < -0.5:
            trend = "very_negative"
        elif avg_score < -0.1:
            trend = "negative"
        else:
            trend = "neutral"
            
        # Collect all emotions
        all_emotions = []
        for entry in self.sentiment_history:
            emotions = entry.get("analysis", {}).get("emotions", [])
            all_emotions.extend(emotions)
            
        # Count emotion frequencies
        emotion_counts = {}
        for emotion in all_emotions:
            if emotion in emotion_counts:
                emotion_counts[emotion] += 1
            else:
                emotion_counts[emotion] = 1
                
        # Get top emotions
        top_emotions = sorted(emotion_counts.items(), 
                             key=lambda x: x[1], 
                             reverse=True)[:3]
            
        return {
            "trend": trend,
            "average_score": avg_score,
            "top_emotions": [emotion for emotion, count in top_emotions],
            "detail": emotion_counts
        }
    
    def get_tailored_response_suggestion(self, sentiment_data):
        """
        Generate a suggestion for how to respond based on sentiment analysis
        
        Args:
            sentiment_data (dict): The sentiment analysis results
            
        Returns:
            str: A suggestion for how to respond
        """
        sentiment = sentiment_data.get("sentiment", "neutral")
        emotions = sentiment_data.get("emotions", [])
        
        if sentiment == "very_negative":
            return "The candidate seems very negative. Consider asking if they have concerns about the process or position that you could address."
            
        elif sentiment == "negative":
            return "The candidate is showing some negative sentiment. Try to be reassuring and highlight positive aspects of the role."
            
        elif sentiment == "very_positive":
            return "The candidate is very enthusiastic! Maintain this energy and delve deeper into their technical expertise."
            
        elif sentiment == "positive":
            return "The candidate is responding positively. This is a good time to ask more challenging questions."
            
        elif "nervous" in emotions or "anxious" in emotions:
            return "The candidate appears nervous. Consider using a more reassuring tone and simpler questions to build confidence."
            
        elif "confused" in emotions:
            return "The candidate seems confused. Try rephrasing your questions more clearly or breaking them down."
            
        elif "confident" in emotions:
            return "The candidate is showing confidence. This is a good opportunity to explore more complex technical scenarios."
            
        else:
            return "The candidate's response is neutral. Proceed with the standard question flow."
    
    def get_sentiment_color(self, sentiment):
        """
        Get a color corresponding to a sentiment for UI display
        
        Args:
            sentiment (str): The sentiment category
            
        Returns:
            str: A hex color code
        """
        sentiment_colors = {
            "very_positive": "#28a745",  # Green
            "positive": "#8bc34a",      # Light green
            "neutral": "#6c757d",       # Gray
            "negative": "#ffc107",      # Yellow
            "very_negative": "#dc3545"  # Red
        }
        
        return sentiment_colors.get(sentiment, "#6c757d")
        
    def get_sentiment_emoji(self, sentiment):
        """
        Get an emoji corresponding to a sentiment for UI display
        
        Args:
            sentiment (str): The sentiment category
            
        Returns:
            str: An emoji representing the sentiment
        """
        sentiment_emojis = {
            "very_positive": "😃",
            "positive": "🙂",
            "neutral": "😐",
            "negative": "🙁",
            "very_negative": "😞"
        }
        
        return sentiment_emojis.get(sentiment, "😐")
        
    def format_sentiment_for_display(self, sentiment_data):
        """
        Format sentiment analysis results for display in the UI
        
        Args:
            sentiment_data (dict): The sentiment analysis results
            
        Returns:
            str: Formatted HTML/Markdown for display
        """
        sentiment = sentiment_data.get("sentiment", "neutral")
        score = sentiment_data.get("score", 0)
        emotions = sentiment_data.get("emotions", [])
        confidence = sentiment_data.get("confidence", 0)
        
        emoji = self.get_sentiment_emoji(sentiment)
        color = self.get_sentiment_color(sentiment)
        
        emotions_text = ", ".join(emotions) if emotions else "None detected"
        
        html = f"""
        <div style="margin: 10px 0; padding: 10px; border-left: 4px solid {color}; background-color: rgba(0,0,0,0.05);">
            <h4 style="margin: 0; color: {color};">{emoji} Sentiment: {sentiment.replace('_', ' ').title()}</h4>
            <p>Score: {score:.2f} | Confidence: {confidence:.2f}</p>
            <p>Emotions: {emotions_text}</p>
        </div>
        """
        
        return html