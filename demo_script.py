"""
Demo script to showcase TalentScout Hiring Assistant functionality
"""

from chatbot import HiringAssistantChatbot
from data_handler import DataHandler
import json

def run_demo_conversation():
    """Run a complete demo conversation"""
    print("🤖 TalentScout Hiring Assistant Demo")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = HiringAssistantChatbot()
    
    # Demo conversation flow
    demo_inputs = [
        "",  # Initial greeting
        "John Smith",  # Name
        "john.smith@email.com",  # Email
        "+1-555-123-4567",  # Phone
        "5",  # Years of experience
        "Full Stack Developer",  # Desired position
        "San Francisco, CA",  # Location
        "Python, Django, React, JavaScript, PostgreSQL, Docker",  # Tech stack
        "Django follows the MVT pattern where Model handles data, View processes requests and returns responses, and Template handles the presentation layer. It's different from MVC as the View acts more like a controller.",  # Answer 1
        "I use Django ORM for database operations, implement proper indexing, use select_related and prefetch_related for query optimization, implement caching with Redis, and use database connection pooling.",  # Answer 2
        "I use React hooks like useState for local state and useEffect for side effects. For complex state, I use useReducer or state management libraries like Redux. I also implement proper component lifecycle management."  # Answer 3
    ]
    
    for i, user_input in enumerate(demo_inputs):
        print(f"\n--- Step {i + 1} ---")
        
        if i == 0:
            print("🤖 Starting conversation...")
        else:
            print(f"👤 User: {user_input}")
        
        response, ended = chatbot.process_message(user_input)
        print(f"🤖 Assistant: {response}")
        
        if ended:
            print("\n✅ Conversation completed!")
            break
    
    # Display final candidate information
    print("\n" + "=" * 50)
    print("📊 FINAL CANDIDATE INFORMATION")
    print("=" * 50)
    
    candidate_info = chatbot.candidate_info.to_dict()
    for key, value in candidate_info.items():
        if key == 'technical_answers':
            print(f"\n📝 Technical Answers:")
            for q_key, q_data in value.items():
                print(f"   Q: {q_data['question']}")
                print(f"   A: {q_data['answer'][:100]}...")
        else:
            print(f"• {key.replace('_', ' ').title()}: {value}")

def test_tech_question_generation():
    """Test technical question generation for different tech stacks"""
    from tech_questions import TechQuestionGenerator
    
    print("\n🧪 TESTING TECH QUESTION GENERATION")
    print("=" * 50)
    
    test_stacks = [
        (["Python", "Django", "PostgreSQL"], 3),
        (["JavaScript", "React", "Node.js"], 5),
        (["Java", "Spring", "MySQL"], 7),
        (["Go", "Kubernetes", "Docker"], 2)
    ]
    
    for tech_stack, experience in test_stacks:
        print(f"\n📚 Tech Stack: {', '.join(tech_stack)} ({experience} years experience)")
        questions = TechQuestionGenerator.generate_questions(tech_stack, experience)
        
        for i, question in enumerate(questions, 1):
            print(f"   {i}. {question}")

def test_data_handling():
    """Test data handling and privacy features"""
    print("\n🔒 TESTING DATA HANDLING & PRIVACY")
    print("=" * 50)
    
    data_handler = DataHandler()
    
    # Test candidate data
    test_candidate = {
        'full_name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'phone': '+1-555-987-6543',
        'experience_years': 4,
        'desired_position': 'Frontend Developer',
        'location': 'New York, NY',
        'tech_stack': ['React', 'TypeScript', 'CSS'],
        'technical_answers': {
            'question_1': {
                'question': 'Explain React hooks',
                'answer': 'React hooks allow functional components to use state and lifecycle methods...'
            }
        }
    }
    
    # Save candidate
    success = data_handler.save_candidate(test_candidate)
    print(f"✅ Candidate saved: {success}")
    
    # Test anonymization
    anonymized = data_handler.anonymize_candidate_data(test_candidate)
    print(f"\n🔒 Original vs Anonymized:")
    print(f"Name: {test_candidate['full_name']} → {anonymized['full_name']}")
    print(f"Email: {test_candidate['email']} → {anonymized['email']}")
    print(f"Phone: {test_candidate['phone']} → {anonymized['phone']}")

def main():
    """Main demo function"""
    print("🎯 TalentScout Hiring Assistant - Complete Demo")
    print("=" * 60)
    
    try:
        # Run demo conversation
        run_demo_conversation()
        
        # Test tech question generation
        test_tech_question_generation()
        
        # Test data handling
        test_data_handling()
        
        print("\n🎉 Demo completed successfully!")
        print("\nTo run the full application:")
        print("1. Install requirements: pip install -r requirements.txt")
        print("2. Run the app: python run_app.py")
        print("   or: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()