"""
TalentScout Hiring Assistant - Streamlit Application
"""

import streamlit as st
import os
from datetime import datetime
from chatbot import HiringAssistantChatbot, ConversationStage
from data_handler import DataHandler

# Page configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        text-align: right;
    }
    .bot-message {
        background-color: #e9ecef;
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
    .status-info {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-info {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = HiringAssistantChatbot()
    
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    
    if 'conversation_ended' not in st.session_state:
        st.session_state.conversation_ended = False
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def display_header():
    """Display application header"""
    st.markdown('<h1 class="main-header">🤖 TalentScout Hiring Assistant</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("Welcome to TalentScout's AI-powered hiring assistant! I'll help you through the initial screening process by gathering your information and asking relevant technical questions.")

def display_sidebar():
    """Display sidebar with conversation status and controls"""
    with st.sidebar:
        st.header("📊 Conversation Status")
        
        # Get conversation summary
        summary = st.session_state.chatbot.get_conversation_summary()
        
        # Display current stage
        stage_emoji = {
            'greeting': '👋',
            'collecting_info': '📝',
            'tech_questions': '💻',
            'conclusion': '✅',
            'ended': '🏁'
        }
        
        current_stage = summary['stage']
        st.write(f"**Current Stage:** {stage_emoji.get(current_stage, '❓')} {current_stage.replace('_', ' ').title()}")
        
        # Display progress
        if current_stage == 'collecting_info':
            candidate_info = summary['candidate_info']
            completed_fields = sum(1 for value in candidate_info.values() if value)
            total_fields = 7  # Total required fields
            progress = completed_fields / total_fields
            st.progress(progress)
            st.write(f"Information collected: {completed_fields}/{total_fields}")
        
        elif current_stage == 'tech_questions':
            questions_total = summary['questions_asked']
            questions_answered = summary['questions_answered']
            if questions_total > 0:
                progress = questions_answered / questions_total
                st.progress(progress)
                st.write(f"Questions answered: {questions_answered}/{questions_total}")
        
        st.markdown("---")
        
        # Control buttons
        if st.button("🔄 Start New Conversation"):
            st.session_state.chatbot = HiringAssistantChatbot()
            st.session_state.conversation_started = False
            st.session_state.conversation_ended = False
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📋 View Candidate Info"):
            display_candidate_info()
        
        # Admin section
        st.markdown("---")
        st.header("🔧 Admin Panel")
        
        if st.button("📊 View All Candidates"):
            display_all_candidates()

def display_candidate_info():
    """Display current candidate information"""
    candidate_info = st.session_state.chatbot.candidate_info.to_dict()
    
    st.subheader("Current Candidate Information")
    
    info_display = {
        'Full Name': candidate_info.get('full_name', 'Not provided'),
        'Email': candidate_info.get('email', 'Not provided'),
        'Phone': candidate_info.get('phone', 'Not provided'),
        'Experience': f"{candidate_info.get('experience_years', 0)} years",
        'Desired Position': candidate_info.get('desired_position', 'Not provided'),
        'Location': candidate_info.get('location', 'Not provided'),
        'Tech Stack': ', '.join(candidate_info.get('tech_stack', [])) or 'Not provided'
    }
    
    for key, value in info_display.items():
        st.write(f"**{key}:** {value}")

def display_all_candidates():
    """Display all candidate records"""
    data_handler = DataHandler()
    candidates = data_handler.get_all_candidates()
    
    st.subheader(f"All Candidates ({len(candidates)} total)")
    
    if not candidates:
        st.info("No candidate records found.")
        return
    
    for i, candidate in enumerate(candidates[-10:], 1):  # Show last 10 candidates
        with st.expander(f"Candidate {i}: {candidate.get('full_name', 'Unknown')}"):
            st.write(f"**Email:** {candidate.get('email', 'N/A')}")
            st.write(f"**Experience:** {candidate.get('experience_years', 0)} years")
            st.write(f"**Position:** {candidate.get('desired_position', 'N/A')}")
            st.write(f"**Tech Stack:** {', '.join(candidate.get('tech_stack', []))}")
            st.write(f"**Timestamp:** {candidate.get('timestamp', 'N/A')}")

def display_chat_interface():
    """Display main chat interface"""
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display conversation history
        for message in st.session_state.messages:
            if message['role'] == 'user':
                st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
    
    # Input area
    st.markdown("---")
    
    # Check if conversation has ended
    if st.session_state.conversation_ended:
        st.success("✅ Conversation completed! Thank you for using TalentScout Hiring Assistant.")
        if st.button("Start New Conversation"):
            st.session_state.chatbot = HiringAssistantChatbot()
            st.session_state.conversation_started = False
            st.session_state.conversation_ended = False
            st.session_state.messages = []
            st.rerun()
        return
    
    # Start conversation if not started
    if not st.session_state.conversation_started:
        if st.button("🚀 Start Screening Process", type="primary"):
            st.session_state.conversation_started = True
            # Get initial greeting
            greeting, _ = st.session_state.chatbot.process_message("")
            st.session_state.messages.append({
                'role': 'assistant',
                'content': greeting,
                'timestamp': datetime.now().isoformat()
            })
            st.rerun()
        return
    
    # Chat input
    user_input = st.chat_input("Type your response here...")
    
    if user_input:
        # Add user message to display
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Process message with chatbot
        response, conversation_ended = st.session_state.chatbot.process_message(user_input)
        
        # Add bot response to display
        st.session_state.messages.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update conversation status
        if conversation_ended:
            st.session_state.conversation_ended = True
        
        st.rerun()

def display_instructions():
    """Display usage instructions"""
    with st.expander("📖 How to Use This Assistant"):
        st.markdown("""
        **Welcome to TalentScout Hiring Assistant!** Here's how the screening process works:
        
        1. **Start the Process**: Click "Start Screening Process" to begin
        2. **Provide Information**: I'll ask for your basic information including:
           - Full name and contact details
           - Years of experience
           - Desired position
           - Current location
           - Technical skills and expertise
        
        3. **Technical Questions**: Based on your tech stack, I'll ask 3-5 relevant technical questions
        4. **Completion**: Once finished, your information will be securely stored for review
        
        **Tips for Best Results:**
        - Be specific about your technical skills
        - Provide complete answers to technical questions
        - You can end the conversation anytime by saying "goodbye" or "exit"
        
        **Privacy Note:** Your information is handled securely and used only for recruitment purposes.
        """)

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Create layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display instructions
        display_instructions()
        
        # Display chat interface
        display_chat_interface()
    
    with col2:
        # Display sidebar content in column
        display_sidebar()

if __name__ == "__main__":
    main()