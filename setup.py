"""
Setup script for Scanofinder
Run: python setup.py
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a shell command"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {command}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("Setting up Scanofinder...")
    print("=" * 50)
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv venv"):
            print("Failed to create virtual environment")
            return
    
    # Determine activation script
    if sys.platform == 'win32':
        activate_script = 'venv\\Scripts\\activate'
        pip_cmd = 'venv\\Scripts\\pip'
        python_cmd = 'venv\\Scripts\\python'
    else:
        activate_script = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
        python_cmd = 'venv/bin/python'
    
    print("\nInstalling dependencies...")
    if not run_command(f"{pip_cmd} install -r requirements.txt"):
        print("Failed to install dependencies")
        return
    
    print("\nCreating .env file if it doesn't exist...")
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ Created .env from .env.example")
            print("⚠ Please edit .env and add your Stripe keys")
        else:
            print("⚠ .env.example not found. Please create .env manually")
    
    print("\nRunning migrations...")
    if not run_command(f"{python_cmd} manage.py makemigrations"):
        print("Failed to create migrations")
        return
    
    if not run_command(f"{python_cmd} manage.py migrate"):
        print("Failed to run migrations")
        return
    
    print("\n" + "=" * 50)
    print("Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file and add your Stripe keys")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Run the server: python manage.py runserver")
    print("4. Access the app at http://localhost:8000")

if __name__ == '__main__':
    main()

