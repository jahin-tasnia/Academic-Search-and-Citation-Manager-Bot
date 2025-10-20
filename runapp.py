"""
Academic Search & Citation Manager — Streamlit Runner
Usage:
    python runapp.py
"""

import subprocess, sys
from pathlib import Path


def check_requirements():
    try:
        import streamlit, langchain, langgraph  # noqa

        print("✅ All required packages are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False


def check_env():
    if Path(".env").exists():
        print("✅ .env found")
        return True
    print("❌ .env not found.\nCreate a .env with:\nGROQ_API_KEY=your_groq_key")
    return False


def main():
    print("🎓 Academic Search & Citation Manager")
    if not check_requirements():
        return
    if not check_env():
        return
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=False
    )


if __name__ == "__main__":
    main()
