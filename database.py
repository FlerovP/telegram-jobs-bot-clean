import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google.cloud import firestore
from google.oauth2 import service_account

load_dotenv()

# Initialize Firestore client
cred = service_account.Credentials.from_service_account_info(
    json.loads(os.getenv('GOOGLE_CREDENTIALS', '{}'))
)
db = firestore.Client(credentials=cred, project='telegram-jobs-bot-v2')

def init_db():
    """Initialize the database (no-op for Firestore)"""
    pass

def create_job(
    title: str,
    company: str = None,
    salary: str = None,
    requirements: str = None,
    link: str = None,
    source: str = None,
    message_id: int = None
):
    """Create a new job entry"""
    try:
        job_data = {
            'title': title,
            'company': company,
            'salary': salary,
            'requirements': requirements,
            'link': link,
            'source': source,
            'message_id': message_id,
            'created_at': firestore.SERVER_TIMESTAMP
        }
        
        # Use message_id as the document ID
        doc_ref = db.collection('jobs').document(str(message_id))
        doc_ref.set(job_data)
        return job_data
    except Exception as e:
        print(f"Error saving job: {e}")
        raise e

def job_exists(message_id: int) -> bool:
    """Check if a job with given message_id exists"""
    try:
        doc_ref = db.collection('jobs').document(str(message_id))
        doc = doc_ref.get()
        return doc.exists
    except Exception as e:
        print(f"Error checking job existence: {e}")
        return False

def get_all_jobs():
    """Get all jobs from database"""
    try:
        jobs_ref = db.collection('jobs')
        jobs = jobs_ref.stream()
        return [job.to_dict() for job in jobs]
    except Exception as e:
        print(f"Error getting all jobs: {e}")
        return [] 