import os
import shutil
from app.config.settings import FAISS_PATH
from app.config.constants import ALL_SHARDS

def rebuild():
    print("WARNING: This will delete all existing vector and keyword indexes.")
    confirm = input("Are you sure you want to proceed? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Aborting rebuild.")
        return

    # 1. Clear FAISS index directory
    if os.path.exists(FAISS_PATH):
        print(f"Clearing directory: {FAISS_PATH}")
        shutil.rmtree(FAISS_PATH)
    
    os.makedirs(FAISS_PATH, exist_ok=True)
    
    print("Indexes cleared.")
    print("To re-populate, ensure the API and Worker are running, then use load_dummy_data.py")

if __name__ == "__main__":
    rebuild()
