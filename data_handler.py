import json
import os
import hashlib
import uuid
from datetime import datetime
import streamlit as st # type: ignore
from cryptography.fernet import Fernet # type: ignore

class DataHandler:
    """
    Class to handle sensitive candidate data with GDPR compliance.
    Provides functionality for:
    - Data anonymization
    - Secure storage
    - Encryption/decryption of sensitive information
    - GDPR compliance features
    """
    
    def __init__(self, encryption_key=None):
        """
        Initialize the DataHandler with an encryption key
        
        Args:
            encryption_key (str, optional): The encryption key. If None, a new one will be generated.
        """
        # Create data directory if it doesn't exist
        self.data_dir = "candidate_data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Set up encryption
        if encryption_key:
            self.key = encryption_key
        else:
            # Generate a key if not provided or stored
            if 'encryption_key' in st.session_state:
                self.key = st.session_state.encryption_key
            else:
                self.key = Fernet.generate_key()
                st.session_state.encryption_key = self.key
        
        self.cipher = Fernet(self.key)
    
    def anonymize_data(self, candidate_info):
        """
        Create an anonymized version of candidate data for analysis purposes
        
        Args:
            candidate_info (dict): The candidate information to anonymize
            
        Returns:
            dict: Anonymized candidate data
        """
        anonymous_data = candidate_info.copy()
        
        # Generate unique anonymous ID based on email
        if anonymous_data.get("email"):
            # Create consistent but anonymous ID
            email_hash = hashlib.sha256(anonymous_data["email"].encode()).hexdigest()[:10]
            anonymous_data["anonymous_id"] = email_hash
        else:
            # If no email, create a random ID
            anonymous_data["anonymous_id"] = uuid.uuid4().hex[:10]
        
        # Remove or mask personally identifiable information
        if anonymous_data.get("name"):
            # Replace name with "Candidate"
            anonymous_data["name"] = f"Candidate-{anonymous_data['anonymous_id']}"
        
        # Mask contact information
        if anonymous_data.get("email"):
            parts = anonymous_data["email"].split("@")
            if len(parts) == 2:
                anonymous_data["email"] = f"{parts[0][0]}{'*' * (len(parts[0])-2)}{parts[0][-1]}@{parts[1]}"
        
        if anonymous_data.get("phone"):
            # Mask phone number, keeping only the last 2 digits
            digits = ''.join(filter(str.isdigit, anonymous_data["phone"]))
            masked_len = max(len(digits) - 2, 0)
            anonymous_data["phone"] = '*' * masked_len + digits[-2:] if len(digits) > 2 else digits
        
        # Keep non-identifying information
        # (experience, desired_position, location, tech_stack)
        
        return anonymous_data

    def encrypt_sensitive_data(self, candidate_info):
        """
        Encrypt sensitive fields in candidate data
        
        Args:
            candidate_info (dict): The candidate information to encrypt
            
        Returns:
            dict: Data with sensitive fields encrypted
        """
        encrypted_data = {}
        sensitive_fields = ["name", "email", "phone"]
        
        for key, value in candidate_info.items():
            if key in sensitive_fields and value:
                # Encrypt sensitive fields
                encrypted_data[key] = self.cipher.encrypt(value.encode()).decode()
            else:
                # Keep non-sensitive fields as is
                encrypted_data[key] = value
        
        return encrypted_data
    
    def decrypt_sensitive_data(self, encrypted_data):
        """
        Decrypt sensitive fields in candidate data
        
        Args:
            encrypted_data (dict): The candidate information with encrypted fields
            
        Returns:
            dict: Data with sensitive fields decrypted
        """
        decrypted_data = {}
        sensitive_fields = ["name", "email", "phone"]
        
        for key, value in encrypted_data.items():
            if key in sensitive_fields and value and isinstance(value, str):
                try:
                    # Attempt to decrypt sensitive fields
                    decrypted_data[key] = self.cipher.decrypt(value.encode()).decode()
                except Exception:
                    # If it wasn't actually encrypted, keep as is
                    decrypted_data[key] = value
            else:
                # Keep non-sensitive fields as is
                decrypted_data[key] = value
        
        return decrypted_data
    
    def save_candidate_data(self, candidate_info, conversation_history=None):
        """
        Save candidate data securely with encryption for sensitive information
        
        Args:
            candidate_info (dict): The candidate information to save
            conversation_history (list, optional): Conversation history to save
            
        Returns:
            str: The filename where data was saved
        """
        if not candidate_info.get("email"):
            # Generate a random ID if no email is available
            file_id = uuid.uuid4().hex
        else:
            # Create a filename based on hashed email for consistency
            file_id = hashlib.sha256(candidate_info["email"].encode()).hexdigest()[:10]
        
        # Create a record with metadata
        record = {
            "timestamp": datetime.now().isoformat(),
            "data_version": "1.0",
            "encrypted_candidate_info": self.encrypt_sensitive_data(candidate_info),
            "anonymized_candidate_info": self.anonymize_data(candidate_info)
        }
        
        # Add conversation history if provided
        if conversation_history:
            # Save only the content, not role information
            sanitized_history = []
            for msg in conversation_history:
                sanitized_history.append({
                    "role": msg.get("role", "unknown"),
                    "content": msg.get("content", "")
                })
            record["conversation_history"] = sanitized_history
        
        # Save to a JSON file
        filename = f"{self.data_dir}/candidate_{file_id}.json"
        with open(filename, "w") as f:
            json.dump(record, f, indent=2)
        
        return filename
    
    def load_candidate_data(self, file_id):
        """
        Load and decrypt candidate data from storage
        
        Args:
            file_id (str): The file ID to load
            
        Returns:
            dict: The loaded and decrypted candidate data or None if not found
        """
        filename = f"{self.data_dir}/candidate_{file_id}.json"
        try:
            with open(filename, "r") as f:
                record = json.load(f)
                
            # Decrypt the candidate info
            if "encrypted_candidate_info" in record:
                decrypted_info = self.decrypt_sensitive_data(record["encrypted_candidate_info"])
                record["candidate_info"] = decrypted_info
                
            return record
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def get_data_deletion_info(self):
        """
        Generate information about data retention and deletion for GDPR compliance
        
        Returns:
            str: Information about data retention and deletion
        """
        return """
        ## Data Privacy Information
        
        Your data is stored securely and encrypted in accordance with GDPR regulations.
        
        - We retain your information for recruitment purposes for up to 6 months.
        - You have the right to request access to, correction, or deletion of your data.
        - To exercise these rights, please contact privacy@talentscout.example.com.
        - For full details on how we handle your data, please see our Privacy Policy.
        """
    
    def get_gdpr_consent_text(self):
        """
        Generate GDPR consent text for candidates
        
        Returns:
            str: GDPR consent text
        """
        return """
        By continuing this conversation, you consent to TalentScout collecting and processing 
        your personal information for recruitment purposes. Your data will be stored securely 
        and in accordance with our Privacy Policy. You may request access to, correction, 
        or deletion of your data at any time.
        """
        
    def generate_simulated_candidates(self, count=5):
        """
        Generate simulated candidate data for testing purposes
        
        Args:
            count (int): Number of simulated candidates to generate
            
        Returns:
            list: List of simulated candidate dictionaries
        """
        simulated_candidates = []
        
        tech_stacks = [
            "Python, Django, PostgreSQL, Docker", 
            "JavaScript, React, Node.js, MongoDB",
            "Java, Spring Boot, MySQL, AWS",
            "C#, .NET Core, SQL Server, Azure",
            "Ruby, Rails, Redis, Heroku",
            "PHP, Laravel, MySQL, Linux",
            "Go, PostgreSQL, Docker, Kubernetes",
            "Swift, iOS, Firebase, Git",
            "Kotlin, Android, SQLite, Jenkins"
        ]
        
        locations = ["New York", "San Francisco", "London", "Berlin", "Toronto", "Mumbai", "Pune", "Delhi", "Gurgaon",
                    "Sydney", "Singapore", "Bangalore", "Tokyo", "Remote"]
        
        positions = ["Software Engineer", "Frontend Developer", "Backend Developer", "MlOps Engineer",
                    "Full Stack Developer", "DevOps Engineer", "Data Scientist", 
                    "Machine Learning Engineer", "Mobile Developer", "QA Engineer"]
        
        for i in range(count):
            # Create a simulated candidate
            candidate = {
                "name": f"Test Candidate {i+1}",
                "email": f"candidate{i+1}@example.com",
                "phone": f"+1555{i:04d}1234",
                "experience": str(i % 10 + 1),
                "desired_position": positions[i % len(positions)],
                "location": locations[i % len(locations)],
                "tech_stack": tech_stacks[i % len(tech_stacks)],
                "questions_asked": bool(i % 2),
                "conversation_complete": bool(i % 3)
            }
            simulated_candidates.append(candidate)
        
        return simulated_candidates