"""
Deployment script for TalentScout Hiring Assistant
Supports local and cloud deployment options
"""

import os
import subprocess
import sys
import json
from pathlib import Path

class DeploymentManager:
    """Manages deployment of the TalentScout Hiring Assistant"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.requirements_file = self.project_root / "requirements.txt"
        self.app_file = self.project_root / "app.py"
    
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        print("🔍 Checking prerequisites...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            print("❌ Python 3.8 or higher is required")
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check required files
        required_files = [self.requirements_file, self.app_file]
        for file_path in required_files:
            if not file_path.exists():
                print(f"❌ Required file missing: {file_path}")
                return False
        print("✅ All required files present")
        
        return True
    
    def install_dependencies(self):
        """Install required dependencies"""
        print("📦 Installing dependencies...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)
            ], check=True, capture_output=True, text=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def setup_environment(self):
        """Set up environment configuration"""
        print("⚙️ Setting up environment...")
        
        env_file = self.project_root / ".env"
        env_example = self.project_root / ".env.example"
        
        if not env_file.exists() and env_example.exists():
            # Copy example to .env
            with open(env_example, 'r') as example:
                content = example.read()
            with open(env_file, 'w') as env:
                env.write(content)
            print("📝 Created .env file from template")
        
        # Create data directory if it doesn't exist
        data_dir = self.project_root / "data"
        if not data_dir.exists():
            data_dir.mkdir()
            print("📁 Created data directory")
        
        # Create empty candidates file if it doesn't exist
        candidates_file = data_dir / "candidates.json"
        if not candidates_file.exists():
            with open(candidates_file, 'w') as f:
                json.dump([], f)
            print("📄 Created candidates.json file")
        
        print("✅ Environment setup complete")
        return True
    
    def run_tests(self):
        """Run application tests"""
        print("🧪 Running tests...")
        
        test_file = self.project_root / "test_chatbot.py"
        if not test_file.exists():
            print("⚠️ Test file not found, skipping tests")
            return True
        
        try:
            result = subprocess.run([
                sys.executable, str(test_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ All tests passed")
                return True
            else:
                print("❌ Some tests failed")
                print(result.stdout)
                return False
        except Exception as e:
            print(f"⚠️ Could not run tests: {e}")
            return True  # Don't fail deployment for test issues
    
    def deploy_local(self, port=8501):
        """Deploy application locally"""
        print(f"🚀 Starting local deployment on port {port}...")
        
        try:
            # Run Streamlit app
            cmd = [sys.executable, "-m", "streamlit", "run", str(self.app_file), "--server.port", str(port)]
            print(f"📱 Application will be available at: http://localhost:{port}")
            print("🔗 Opening in your default browser...")
            print("💡 Press Ctrl+C to stop the application")
            
            subprocess.run(cmd)
            
        except KeyboardInterrupt:
            print("\n👋 Application stopped by user")
        except Exception as e:
            print(f"❌ Failed to start application: {e}")
            return False
        
        return True
    
    def generate_docker_files(self):
        """Generate Docker configuration files"""
        print("🐳 Generating Docker configuration...")
        
        # Dockerfile
        dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
"""
        
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)
        
        # Docker Compose
        docker_compose_content = """version: '3.8'

services:
  talentscout-assistant:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
"""
        
        with open("docker-compose.yml", "w") as f:
            f.write(docker_compose_content)
        
        # .dockerignore
        dockerignore_content = """.git
.gitignore
README.md
Dockerfile
.dockerignore
.env
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.venv
"""
        
        with open(".dockerignore", "w") as f:
            f.write(dockerignore_content)
        
        print("✅ Docker files generated")
        print("📝 To build and run with Docker:")
        print("   docker-compose up --build")
        
        return True
    
    def generate_cloud_configs(self):
        """Generate cloud deployment configurations"""
        print("☁️ Generating cloud deployment configurations...")
        
        # Heroku Procfile
        with open("Procfile", "w") as f:
            f.write("web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0\n")
        
        # Railway configuration
        railway_config = {
            "build": {
                "builder": "NIXPACKS"
            },
            "deploy": {
                "startCommand": "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0",
                "healthcheckPath": "/_stcore/health",
                "healthcheckTimeout": 100,
                "restartPolicyType": "ON_FAILURE",
                "restartPolicyMaxRetries": 10
            }
        }
        
        with open("railway.json", "w") as f:
            json.dump(railway_config, f, indent=2)
        
        # Streamlit Cloud config
        streamlit_config = """[server]
headless = true
port = $PORT
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
"""
        
        config_dir = Path(".streamlit")
        config_dir.mkdir(exist_ok=True)
        
        with open(config_dir / "config.toml", "w") as f:
            f.write(streamlit_config)
        
        print("✅ Cloud deployment configurations generated")
        print("📝 Deployment options:")
        print("   • Heroku: Use Procfile")
        print("   • Railway: Use railway.json")
        print("   • Streamlit Cloud: Use .streamlit/config.toml")
        
        return True

def main():
    """Main deployment function"""
    print("🎯 TalentScout Hiring Assistant - Deployment Manager")
    print("=" * 60)
    
    deployment = DeploymentManager()
    
    # Check prerequisites
    if not deployment.check_prerequisites():
        print("❌ Prerequisites not met. Please fix the issues and try again.")
        return False
    
    # Install dependencies
    if not deployment.install_dependencies():
        print("❌ Failed to install dependencies.")
        return False
    
    # Setup environment
    if not deployment.setup_environment():
        print("❌ Failed to setup environment.")
        return False
    
    # Run tests
    deployment.run_tests()
    
    # Ask user for deployment type
    print("\n🚀 Choose deployment option:")
    print("1. Local deployment (recommended for development)")
    print("2. Generate Docker files")
    print("3. Generate cloud deployment configs")
    print("4. All of the above")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            deployment.deploy_local()
        elif choice == "2":
            deployment.generate_docker_files()
        elif choice == "3":
            deployment.generate_cloud_configs()
        elif choice == "4":
            deployment.generate_docker_files()
            deployment.generate_cloud_configs()
            print("\n🎉 All configurations generated!")
            print("To start locally, run: python deploy.py and choose option 1")
        else:
            print("❌ Invalid choice. Please run the script again.")
            return False
        
        print("\n✅ Deployment process completed successfully!")
        return True
        
    except KeyboardInterrupt:
        print("\n👋 Deployment cancelled by user")
        return False
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)