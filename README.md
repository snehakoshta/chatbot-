# TalentScout Hiring Assistant Chatbot

## Project Overview
An intelligent Hiring Assistant chatbot for TalentScout, a fictional recruitment agency specializing in technology placements. The chatbot assists in initial candidate screening by gathering essential information and generating relevant technical questions based on the candidate's declared tech stack.

## Features
- **Interactive UI**: Clean Streamlit interface for seamless candidate interaction
- **Information Gathering**: Collects candidate details (name, contact, experience, etc.)
- **Tech Stack Assessment**: Generates tailored technical questions based on declared technologies
- **Context Management**: Maintains conversation flow and handles follow-up questions
- **Fallback Mechanism**: Handles unexpected inputs gracefully
- **Data Privacy**: Secure handling of candidate information

## Installation Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps
1. Clone the repository:
```bash
git clone <repository-url>
cd talentscout-hiring-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file and add your API keys
OPENAI_API_KEY=your_openai_api_key_here
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage Guide
1. Open the application in your browser (typically http://localhost:8501)
2. Start the conversation with the chatbot
3. Provide your information when prompted
4. Declare your tech stack
5. Answer the generated technical questions
6. Complete the screening process

## Technical Details

### Libraries Used
- **Streamlit**: Frontend interface development
- **OpenAI**: Language model integration
- **Python-dotenv**: Environment variable management
- **JSON**: Data handling and storage

### Architecture
- Modular design with separate components for UI, chatbot logic, and data handling
- State management using Streamlit session state
- Prompt engineering for context-aware conversations

## Prompt Design
The chatbot uses carefully crafted prompts to:
- Guide information gathering in a natural conversation flow
- Generate relevant technical questions based on tech stack
- Maintain context throughout the interaction
- Handle edge cases and unexpected inputs

## Challenges & Solutions
- **Context Management**: Implemented session state to maintain conversation history
- **Dynamic Question Generation**: Created tech stack mapping for relevant questions
- **Data Privacy**: Implemented secure data handling with anonymization options
- **User Experience**: Designed intuitive conversation flow with clear instructions

## Project Structure
```
talentscout-hiring-assistant/
├── app.py                 # Main Streamlit application
├── chatbot.py            # Core chatbot logic
├── prompts.py            # Prompt templates and engineering
├── data_handler.py       # Data processing and storage
├── tech_questions.py     # Technical question generation
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # Project documentation
├── run_app.py           # Simple application runner
├── demo_script.py       # Demo and testing script
├── test_chatbot.py      # Unit tests
├── deploy.py            # Deployment manager
└── data/                # Candidate data storage
    └── candidates.json  # Simulated candidate database
```

## Quick Start

### Option 1: Using the deployment script (Recommended)
```bash
python deploy.py
```
This will automatically:
- Check prerequisites
- Install dependencies
- Set up environment
- Run tests
- Start the application

### Option 2: Manual setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Option 3: Using the runner script
```bash
python run_app.py
```

## Testing

Run the demo to see all features:
```bash
python demo_script.py
```

Run unit tests:
```bash
python test_chatbot.py
```

## Deployment Options

### Local Development
- Use `python deploy.py` and choose option 1
- Or run `streamlit run app.py` directly

### Docker Deployment
1. Generate Docker files: `python deploy.py` (option 2)
2. Build and run: `docker-compose up --build`

### Cloud Deployment
The project includes configurations for:
- **Heroku**: Uses `Procfile`
- **Railway**: Uses `railway.json`
- **Streamlit Cloud**: Uses `.streamlit/config.toml`
- **AWS/GCP**: Docker-based deployment

Generate cloud configs: `python deploy.py` (option 3)

## License
This project is for educational purposes as part of an AI/ML internship assignment.