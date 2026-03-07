from dotenv import load_dotenv
from google import genai
import json
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def score_job(cv_data:dict, job:dict) -> dict :
    """
    Send to cv_data and job to Gemini
    
    """
    prompt = f"""
    You are a professional recruiter.

    Candidate Profile:
    - Skills: {cv_data["skills"]}
    - Experience: {cv_data["experience_years"]} years
    - Current Title: {cv_data["current_title"]}
    - Education: {cv_data["education"]}
    - Summary: {cv_data["summary"]}

    Job Description:
    {job["job_description"]}
    {job["job_title"]}

    Candidate Profile and job Description and job title analiyse together and 
    return  as a JSON file 
    - match_score ( match_score (integer between 0 and 100)  %
    - match_reason (string)
    - missing_skills  list of skills mentioned in the job description 
    that the candidate does NOT have in their profile.
    Return empty list [] if no skills are missing.

    Return ONLY the JSON, nothing else.

    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    clean_response_data = response.text.strip().replace("```json", "").replace("```","")

    return json.loads(clean_response_data)

if __name__ == "__main__":
    """
    # test cv data
    test_cv = {
        "skills": ["Python", "FastAPI", "SQL"],
        "experience_years": 3,
        "current_title": "Backend Developer",
        "education": "BSc Computer Science",
        "summary": "We need Python, FastAPI, Docker, Kubernetes and AWS experience"
    }
    
    # test job
    test_job = {
        "job_title": "Python Developer",
        "job_description": "We need a Python developer with FastAPI and SQL experience"
    }

    result = score_job(test_cv, test_job)

    
    print(f"Match Score:{result['match_score']}%")
    print(f"Reason:{result['match_reason']}")


    for missing_skills in result['missing_skills']:
        if (len(result['missing_skills'])) != 0:
            print("Missing Skills:")
            print(missing_skills) 
    """


