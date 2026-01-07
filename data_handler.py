"""
Data handling and storage for candidate information
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class DataHandler:
    """Handles candidate data storage and retrieval with privacy considerations"""
    
    def __init__(self, data_dir: str = "data", candidate_file: str = "candidates.json"):
        self.data_dir = data_dir
        self.candidate_file = candidate_file
        self.file_path = os.path.join(data_dir, candidate_file)
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Create empty candidates file if it doesn't exist
        if not os.path.exists(self.file_path):
            self._save_data([])
    
    def save_candidate(self, candidate_data: Dict) -> bool:
        """
        Save candidate information to storage
        
        Args:
            candidate_data (Dict): Candidate information dictionary
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            # Add metadata
            candidate_data['timestamp'] = datetime.now().isoformat()
            candidate_data['id'] = self._generate_candidate_id()
            
            # Load existing data
            existing_data = self._load_data()
            
            # Add new candidate
            existing_data.append(candidate_data)
            
            # Save updated data
            self._save_data(existing_data)
            
            return True
            
        except Exception as e:
            print(f"Error saving candidate data: {e}")
            return False
    
    def get_all_candidates(self) -> List[Dict]:
        """
        Retrieve all candidate records
        
        Returns:
            List[Dict]: List of all candidate records
        """
        return self._load_data()
    
    def get_candidate_by_id(self, candidate_id: str) -> Optional[Dict]:
        """
        Retrieve specific candidate by ID
        
        Args:
            candidate_id (str): Candidate ID
            
        Returns:
            Optional[Dict]: Candidate data if found, None otherwise
        """
        candidates = self._load_data()
        for candidate in candidates:
            if candidate.get('id') == candidate_id:
                return candidate
        return None
    
    def anonymize_candidate_data(self, candidate_data: Dict) -> Dict:
        """
        Anonymize sensitive candidate information for privacy
        
        Args:
            candidate_data (Dict): Original candidate data
            
        Returns:
            Dict: Anonymized candidate data
        """
        anonymized = candidate_data.copy()
        
        # Anonymize sensitive fields
        if 'full_name' in anonymized:
            anonymized['full_name'] = self._anonymize_name(anonymized['full_name'])
        
        if 'email' in anonymized:
            anonymized['email'] = self._anonymize_email(anonymized['email'])
        
        if 'phone' in anonymized:
            anonymized['phone'] = self._anonymize_phone(anonymized['phone'])
        
        return anonymized
    
    def _load_data(self) -> List[Dict]:
        """Load candidate data from storage"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_data(self, data: List[Dict]):
        """Save candidate data to storage"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _generate_candidate_id(self) -> str:
        """Generate unique candidate ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"CAND_{timestamp}"
    
    def _anonymize_name(self, name: str) -> str:
        """Anonymize candidate name"""
        if not name:
            return name
        
        parts = name.split()
        if len(parts) == 1:
            return f"{parts[0][0]}***"
        else:
            return f"{parts[0][0]}*** {parts[-1][0]}***"
    
    def _anonymize_email(self, email: str) -> str:
        """Anonymize email address"""
        if not email or '@' not in email:
            return email
        
        local, domain = email.split('@', 1)
        if len(local) <= 2:
            anonymized_local = local
        else:
            anonymized_local = f"{local[:2]}***"
        
        return f"{anonymized_local}@{domain}"
    
    def _anonymize_phone(self, phone: str) -> str:
        """Anonymize phone number"""
        if not phone:
            return phone
        
        # Keep only last 4 digits visible
        if len(phone) > 4:
            return f"***-***-{phone[-4:]}"
        else:
            return "***-***-****"

class CandidateInfo:
    """Data class for candidate information structure"""
    
    def __init__(self):
        self.full_name = ""
        self.email = ""
        self.phone = ""
        self.experience_years = 0
        self.desired_position = ""
        self.location = ""
        self.tech_stack = []
        self.technical_answers = {}
    
    def to_dict(self) -> Dict:
        """Convert candidate info to dictionary"""
        return {
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'experience_years': self.experience_years,
            'desired_position': self.desired_position,
            'location': self.location,
            'tech_stack': self.tech_stack,
            'technical_answers': self.technical_answers
        }
    
    def from_dict(self, data: Dict):
        """Load candidate info from dictionary"""
        self.full_name = data.get('full_name', '')
        self.email = data.get('email', '')
        self.phone = data.get('phone', '')
        self.experience_years = data.get('experience_years', 0)
        self.desired_position = data.get('desired_position', '')
        self.location = data.get('location', '')
        self.tech_stack = data.get('tech_stack', [])
        self.technical_answers = data.get('technical_answers', {})
    
    def is_complete(self) -> bool:
        """Check if all required information is collected"""
        required_fields = [
            self.full_name,
            self.email,
            self.phone,
            self.desired_position,
            self.location,
            self.tech_stack
        ]
        
        return all(field for field in required_fields) and self.experience_years >= 0
    
    def get_missing_fields(self) -> List[str]:
        """Get list of missing required fields in order"""
        missing = []
        
        if not self.full_name:
            missing.append('Full Name')
        elif not self.email:
            missing.append('Email Address')
        elif not self.phone:
            missing.append('Phone Number')
        elif self.experience_years < 0:
            missing.append('Years of Experience')
        elif not self.desired_position:
            missing.append('Desired Position')
        elif not self.location:
            missing.append('Current Location')
        elif not self.tech_stack:
            missing.append('Tech Stack')
            
        return missing