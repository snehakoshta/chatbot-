"""
Core chatbot logic for TalentScout Hiring Assistant
"""

import re
from typing import Dict, List, Tuple, Optional
from enum import Enum
from prompts import PromptTemplates, PromptBuilder
from tech_questions import TechQuestionGenerator
from data_handler import CandidateInfo, DataHandler

class ConversationStage(Enum):
    """Enumeration of conversation stages"""
    GREETING = "greeting"
    COLLECTING_INFO = "collecting_info"
    TECH_QUESTIONS = "tech_questions"
    CONCLUSION = "conclusion"
    ENDED = "ended"

class HiringAssistantChatbot:
    """Main chatbot class for handling hiring conversations"""
    
    def __init__(self):
        self.conversation_history = []
        self.candidate_info = CandidateInfo()
        self.current_stage = ConversationStage.GREETING
        self.current_question_index = 0
        self.technical_questions = []
        self.data_handler = DataHandler()
        
        # Conversation ending keywords
        self.ending_keywords = [
            'goodbye', 'bye', 'exit', 'quit', 'end', 'stop', 
            'thanks', 'thank you', 'done', 'finish', 'complete'
        ]
    
    def process_message(self, user_input: str) -> Tuple[str, bool]:
        """
        Process user input and generate appropriate response
        
        Args:
            user_input (str): User's message
            
        Returns:
            Tuple[str, bool]: (response_message, is_conversation_ended)
        """
        # Add user message to history
        self.conversation_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': self._get_timestamp()
        })
        
        # Check for conversation ending
        if self._is_ending_conversation(user_input):
            response = self._handle_conversation_ending()
            return response, True
        
        # Process based on current stage
        if self.current_stage == ConversationStage.GREETING:
            response = self._handle_greeting(user_input)
        elif self.current_stage == ConversationStage.COLLECTING_INFO:
            response = self._handle_info_collection(user_input)
        elif self.current_stage == ConversationStage.TECH_QUESTIONS:
            response = self._handle_tech_questions(user_input)
        elif self.current_stage == ConversationStage.CONCLUSION:
            response = self._handle_conclusion(user_input)
        else:
            response = self._handle_fallback(user_input)
        
        # Add bot response to history
        self.conversation_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': self._get_timestamp()
        })
        
        return response, self.current_stage == ConversationStage.ENDED
    
    def _handle_greeting(self, user_input: str) -> str:
        """Handle initial greeting and start information collection"""
        if not user_input.strip():
            return self._get_greeting_message()
        
        # Extract name if provided
        name = self._extract_name(user_input)
        if name:
            self.candidate_info.full_name = name
            self.current_stage = ConversationStage.COLLECTING_INFO
            return f"Nice to meet you, {name}! Let me gather some information for your application. Could you please provide your email address?"
        else:
            return "Thank you for your interest! To get started, could you please tell me your full name?"
    
    def _handle_info_collection(self, user_input: str) -> str:
        """Handle information collection phase"""
        # Determine what information to collect next
        missing_fields = self.candidate_info.get_missing_fields()
        
        if not missing_fields:
            # All info collected, move to technical questions
            self.current_stage = ConversationStage.TECH_QUESTIONS
            self.technical_questions = TechQuestionGenerator.generate_questions(
                self.candidate_info.tech_stack, 
                self.candidate_info.experience_years
            )
            self.current_question_index = 0
            
            if self.technical_questions:
                return f"Great! I have all your information. Now I'd like to ask you some technical questions based on your tech stack. Here's the first question:\n\n1. {self.technical_questions[0]}"
            else:
                return self._move_to_conclusion()
        
        # Process current input and ask for next missing field
        return self._process_info_input(user_input, missing_fields)
    
    def _handle_tech_questions(self, user_input: str) -> str:
        """Handle technical questions phase"""
        if not self.technical_questions:
            return self._move_to_conclusion()
        
        # Store the answer
        if self.current_question_index < len(self.technical_questions):
            question = self.technical_questions[self.current_question_index]
            self.candidate_info.technical_answers[f"question_{self.current_question_index + 1}"] = {
                'question': question,
                'answer': user_input
            }
        
        # Move to next question
        self.current_question_index += 1
        
        if self.current_question_index < len(self.technical_questions):
            next_question = self.technical_questions[self.current_question_index]
            return f"Thank you for your answer. Here's question {self.current_question_index + 1}:\n\n{self.current_question_index + 1}. {next_question}"
        else:
            # All questions answered, move to conclusion
            return self._move_to_conclusion()
    
    def _handle_conclusion(self, user_input: str) -> str:
        """Handle conversation conclusion"""
        self.current_stage = ConversationStage.ENDED
        return "Thank you for your time! If you have any questions about the process, feel free to ask. Otherwise, have a great day!"
    
    def _handle_fallback(self, user_input: str) -> str:
        """Handle unexpected or unclear input"""
        return "I'm sorry, I didn't quite understand that. Could you please rephrase your response? I'm here to help with your job application process."
    
    def _handle_conversation_ending(self) -> str:
        """Handle conversation ending"""
        # Save candidate data if we have meaningful information
        if self.candidate_info.full_name or self.candidate_info.email:
            self.data_handler.save_candidate(self.candidate_info.to_dict())
        
        self.current_stage = ConversationStage.ENDED
        return """Thank you for your time and interest in TalentScout! 

Here's what happens next:
• Your information has been recorded securely
• Our recruitment team will review your responses
• You'll hear back from us within 2-3 business days
• If selected, we'll schedule a detailed interview

Have a great day and good luck with your job search!"""
    
    def _process_info_input(self, user_input: str, missing_fields: List[str]) -> str:
        """Process user input for information collection"""
        next_field = missing_fields[0]
        
        if next_field == 'Email Address':
            email = self._extract_email(user_input)
            if email:
                self.candidate_info.email = email
                return "Perfect! Now, could you please provide your phone number?"
            else:
                return "I need a valid email address. Could you please provide your email?"
        
        elif next_field == 'Phone Number':
            phone = self._extract_phone(user_input)
            if phone:
                self.candidate_info.phone = phone
                return "Great! How many years of professional experience do you have?"
            else:
                return "Please provide a valid phone number."
        
        elif next_field == 'Years of Experience':
            years = self._extract_years(user_input)
            if years is not None:
                self.candidate_info.experience_years = years
                return "Excellent! What position(s) are you interested in applying for?"
            else:
                return "Please provide your years of experience as a number (e.g., 3, 5, 10)."
        
        elif next_field == 'Desired Position':
            self.candidate_info.desired_position = user_input.strip()
            return "Thank you! What's your current location (city, state/country)?"
        
        elif next_field == 'Current Location':
            self.candidate_info.location = user_input.strip()
            return "Almost done! Please list your tech stack - the programming languages, frameworks, databases, and tools you're proficient in. You can separate them with commas."
        
        elif next_field == 'Tech Stack':
            tech_stack = self._extract_tech_stack(user_input)
            if tech_stack:
                self.candidate_info.tech_stack = tech_stack
                return f"Perfect! I've recorded your tech stack: {', '.join(tech_stack)}. Let me prepare some technical questions for you."
            else:
                return "Please provide your technical skills (e.g., Python, React, MySQL, Docker)."
        
        return "I didn't understand that. Could you please try again?"
    
    def _move_to_conclusion(self) -> str:
        """Move conversation to conclusion stage"""
        # Save candidate data
        self.data_handler.save_candidate(self.candidate_info.to_dict())
        self.current_stage = ConversationStage.CONCLUSION
        
        return """Excellent! I've completed the initial screening process. 

Here's a summary of what we covered:
• Personal information collected ✓
• Technical background assessed ✓
• Your responses have been recorded ✓

Thank you for taking the time to complete this screening. Our recruitment team will review your information and technical responses. You can expect to hear back from us within 2-3 business days.

Is there anything else you'd like to know about TalentScout or the application process?"""
    
    def _get_greeting_message(self) -> str:
        """Get initial greeting message"""
        return """Hello! Welcome to TalentScout! 👋

I'm your AI Hiring Assistant, and I'm here to help with your initial screening process. I'll be gathering some basic information about you and asking a few technical questions based on your expertise.

This should take about 5-10 minutes, and it will help our recruitment team better understand your background and skills.

To get started, could you please tell me your full name?"""
    
    def _is_ending_conversation(self, user_input: str) -> bool:
        """Check if user wants to end conversation"""
        user_input_lower = user_input.lower().strip()
        return any(keyword in user_input_lower for keyword in self.ending_keywords)
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Extract name from user input"""
        # Simple name extraction - look for capitalized words
        text = text.strip()
        if len(text.split()) >= 2:
            words = text.split()
            # Check if it looks like a name (capitalized words)
            if all(word[0].isupper() for word in words[:2] if word.isalpha()):
                return ' '.join(words[:2])
        elif len(text.split()) == 1 and text.isalpha() and text[0].isupper():
            return text
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email from user input"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group() if match else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from user input"""
        # Remove all non-digit characters and check length
        digits = re.sub(r'\D', '', text)
        if 10 <= len(digits) <= 15:
            return text.strip()
        return None
    
    def _extract_years(self, text: str) -> Optional[int]:
        """Extract years of experience from user input"""
        # Look for numbers in the text
        numbers = re.findall(r'\d+', text)
        if numbers:
            years = int(numbers[0])
            if 0 <= years <= 50:  # Reasonable range
                return years
        return None
    
    def _extract_tech_stack(self, text: str) -> List[str]:
        """Extract tech stack from user input"""
        # Split by common separators and clean up
        separators = [',', ';', '|', '\n', ' and ', ' & ']
        tech_list = [text]
        
        for sep in separators:
            new_list = []
            for item in tech_list:
                new_list.extend(item.split(sep))
            tech_list = new_list
        
        # Clean and filter
        tech_stack = []
        for tech in tech_list:
            tech = tech.strip().lower()
            if tech and len(tech) > 1:
                tech_stack.append(tech)
        
        return tech_stack[:10]  # Limit to 10 technologies
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of current conversation state"""
        return {
            'stage': self.current_stage.value,
            'candidate_info': self.candidate_info.to_dict(),
            'questions_asked': len(self.technical_questions),
            'questions_answered': self.current_question_index,
            'conversation_length': len(self.conversation_history)
        }