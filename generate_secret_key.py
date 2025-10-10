"""
Generate a secure SECRET_KEY for your FastAPI application
Run this script: python generate_secret_key.py
"""
import secrets

def generate_secret_key():
    # Generate a secure random string
    secret_key = secrets.token_urlsafe(32)
    
    print("=" * 60)
    print("🔑 Your Generated SECRET_KEY:")
    print("=" * 60)
    print(f"\n{secret_key}\n")
    print("=" * 60)
    print("\n📝 Add this to your .env file:")
    print(f"SECRET_KEY={secret_key}")
    print("=" * 60)
    
    return secret_key

if __name__ == "__main__":
    generate_secret_key()

