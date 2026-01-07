"""
Simple script to run the TalentScout Hiring Assistant
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import openai
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main function to run the application"""
    print("🤖 TalentScout Hiring Assistant")
    print("=" * 40)
    
    # Check if requirements are met
    if not check_requirements():
        return
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found. Creating from template...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as example:
                content = example.read()
            with open('.env', 'w') as env_file:
                env_file.write(content)
            print("📝 Created .env file. Please add your OpenAI API key if needed.")
    
    print("🚀 Starting TalentScout Hiring Assistant...")
    print("📱 The application will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("\n💡 To stop the application, press Ctrl+C in this terminal")
    print("=" * 40)
    
    try:
        # Run Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()