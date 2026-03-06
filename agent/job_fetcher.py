from google import genai
from dotenv import load_dotenv
from pprint import pprint
from nuwan_colors import Colors, Texts
from pprint import pprint
import requests
import json
import os

# Load env. to envirament 
load_dotenv()

def fetch_jobs(quary:str, location:str, num_result:int=10) -> list:
    """
    Request to Jsearch api
    retutn job list JSON
    """
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": os.getenv("J_SEARCH_API"),
        "X-RapidAPI-Host":"jsearch.p.rapidapi.com"
    }

    params = {
        "query" : f"{quary} in {location}",
        "page"  : 1,
        "country":"sri lanka",
        "date_posted":"all"
    }

    response = requests.get(url=url, headers=headers, params=params)
    print(Colors.green(f"HTTP status: {response.status_code }"))

    data = response.json()
    #pprint(data['data'])

    if data["status"] != "OK":
        print(Colors.red("Error. JSearch API not ok"))
        return []

    jobs = []

    for job in data['data']:
        jobs.append({
            "job_id": job["job_id"],
            "job_title": job["job_title"],
            "company": job["employer_name"],
            "location": job["job_city"],
            "job_url": job["job_apply_link"],
            "job_description": job["job_description"]
        })

    pprint(jobs)
    return jobs
    
if __name__ == "__main__":
    fetch_jobs("Ayurvedic doctor", "Colombo")