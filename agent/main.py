from supabase import create_client
from dotenv import load_dotenv
from nuwan_colors import Colors, Texts 
from google import genai
import os 
from pprint import pprint

# Internal modules
from cv_parser import parse_pdf, save_cv_to_superbase   # Parses PDF resume into structured data and persists it to the Supabase cv_profile table
from job_fetcher import fetch_jobs                      # Retrieves job listings from the external jobs API based on candidate profile
from scorer import score_job                            # Uses Gemini AI to evaluate job-CV compatibility and returns a relevance score with summary
from email_sender import send_job_matches               # Composes and dispatches a HTML-formatted email containing ranked job matches

# Load env files 
load_dotenv()

# Connect to Gemini 
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Api connection 
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=""
)

# Connect to Supabase 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPERBASE_ANON_KEY")

supabase = create_client(url, key)


def get_active_users() -> dict:
    """
    Get subscription Active users data from Supabase database 
    """

    results = supabase.table("subscriptions").select("*, users(*, cv_profiles(*))").eq("status", "active").execute()

    """
    for result in results.data:
        database = f"Name: {result['users']['full_name']}\nEmail: {result['users']['email']}\nPlan: {result['plan']}"    

    print(database)
    """
    pprint(results.data)

    print(Colors.green("Selected Active Users"))

    return results.data

def agent_run():
    """
    Daily Agent runs 

    """
    print(Colors.green("Supabase Connecting...."))

    # Active users data base 
    active_users = get_active_users()

    for active_user in active_users:
        refer_job = active_user['users']['preferred_job']
        job_location = active_user['users']['location_pref']
        cv_data = active_user['users']['cv_profiles'][0]

        user_name = active_user['users']['full_name'].split()[0]
        user_email = active_user['users']['email']
        
        print(cv_data)
        
        email_job_list = []

        # Find Jobs 
        jobs = fetch_jobs(query=refer_job, location=job_location);
        

        print(Colors.green("Collecting CV Data.... "))

        # Gemini Analyze data 
        for job in jobs:
            gemini_data = score_job(cv_data=cv_data, job=job)
            email_job_list.append({
                "job_title": job['job_title'],
                "company":   job['company'],
                "location":  job['location'],
                "job_url":   job['job_url'],
                "match_score": gemini_data['match_score'],
                "match_reason": gemini_data['match_reason'],
                "missing_skills": gemini_data['missing_skills']
                })
            
            
            #pprint(result)

        print(Colors.green("Getting ready to send email....."))

        send_job_matches(to_email=user_email, name=user_name, jobs=email_job_list)

        print(Colors.green("Email sent"))

         
if __name__ == "__main__":
    agent_run()
    #get_active_users()

# Test connection

#result = supabase.table("users").select("*").execute()
#print("Connected! Users in databse:", len(result.data))

#print(response.text)


