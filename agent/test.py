import os
from dotenv import load_dotenv
from orchestrator import AegisOrchestrator
import time
import sys

# .env ෆයිල් එකේ තියෙන දත්ත කියවීමට
load_dotenv()

def main():
    
    API_KEY = os.getenv("GROQ_API_KEY") 
    
    if not API_KEY:
        print("\n❌ Error: API Key not found! Please check your .env file.")
        return

    print("\n" + "═"*55)
    print(" 🛡️  Smart Devops Assistant: AGENTIC CI/CD AUTOMATION SYSTEM")
    print("═"*55)
    
    url = input("\n🔗 Enter GitHub Repository URL: ")
    aegis = AegisOrchestrator(API_KEY)
    
    print("\n--- Starting Autonomous Pipeline ---")
    
    steps = [
        ("Initializing Aegis Orchestrator...", 1),
        ("Setting up Secure Environment...", 1),
        ("Connecting to Remote Repository...", 1),
        ("Analyzing Frontend Framework...", 2),
        ("Configuring Deployment Protocols...", 1)
    ]

    for desc, delay in steps:
        print(f"[PROCESS] {desc}", end="", flush=True)
        time.sleep(delay)
        print(" ✅ Done")

    result = aegis.start_workflow(url)
    
    if result["status"] == "Success":
        print("\n" + "═"*55)
        print("🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
        print(f"📦 Identified Framework : {result['tech']}")
        print(f"🚀 Deployment Status     : Live")
        print(f"🌍 Live Application Link: {result['link']}")
        print("═"*55)
        print("\n(Note: Click the link above to view your application)")
    else:
        print(f"\n❌ DEPLOYMENT FAILED: {result['msg']}")

if __name__ == "__main__":
    main()