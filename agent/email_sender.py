import resend
from dotenv import load_dotenv
import os

load_dotenv()

resend.api_key = os.getenv("RESEND_API")



def build_html_email(name, jobs):
    """
    Build beautiful HTML email
    """
    # build job cards
    job_cards = ""
    for i, job in enumerate(jobs, 1):
        
        # build missing skills line
        missing = ""
        if job['missing_skills']:
            missing = f"""
            <p style="color:#e74c3c; margin:5px 0;">
                ❌ Missing: {', '.join(job['missing_skills'])}
            </p>"""

        job_cards += f"""
        <div style="background:#f9f9f9; border-left:4px solid #2ecc71; 
                    padding:15px; margin:15px 0; border-radius:4px;">
            <h3 style="margin:0; color:#2c3e50;">
                #{i} {job['job_title']}
            </h3>
            <p style="color:#7f8c8d; margin:5px 0;">
                🏢 {job['company']} • 📍 {job['location']}
            </p>
            <p style="color:#27ae60; font-size:20px; 
                      font-weight:bold; margin:5px 0;">
                🎯 {job['match_score']}% Match
            </p>
            <p style="color:#2c3e50; margin:5px 0;">
                ✅ {job['match_reason']}
            </p>
            {missing}
            <a href="{job['job_url']}" 
               style="display:inline-block; margin-top:10px;
                      background:#2ecc71; color:white; 
                      padding:8px 20px; border-radius:4px; 
                      text-decoration:none; font-weight:bold;">
                Apply Now →
            </a>
        </div>
        """

    # full email template
    html = f"""
    <html>
    <body style="font-family:Arial, sans-serif; 
                 max-width:600px; margin:0 auto; padding:20px;">
        
        <!-- Header -->
        <div style="background:#2ecc71; padding:20px; 
                    border-radius:8px; text-align:center;">
            <h1 style="color:white; margin:0;">🎯 Xearch AI</h1>
            <p style="color:white; margin:5px 0;">
                Your Daily Job Matches
            </p>
        </div>

        <!-- Greeting -->
        <p style="color:#2c3e50; font-size:16px; margin:20px 0;">
            Hi <strong>{name}</strong>, here are your 
            top job matches today:
        </p>

        <!-- Job Cards -->
        {job_cards}

        <!-- Footer -->
        <div style="text-align:center; margin-top:30px; 
                    padding-top:20px; border-top:1px solid #eee;">
            <p style="color:#95a5a6; font-size:12px;">
                Powered by Xearch AI • 
                <a href="#" style="color:#2ecc71;">
                    Unsubscribe
                </a>
            </p>
        </div>

    </body>
    </html>
    """
    return html

def send_job_matches(to_email:str, name:str, jobs:list):
    html = build_html_email(name, jobs)
    
    params: resend.Emails.SendParams = {
        "from": "Jobseeking-ai <jobs@xearchai.com>",
        "to": [to_email],
        "subject": f"🎯 Your Daily Job Matches — {len(jobs)} Jobs Found",
        "html": html,
    }

    email = resend.Emails.send(params)
    print(email)

if __name__ == "__main__":
    test_jobs = [
        {
            "job_title": "Python Developer",
            "company": "Google",
            "location": "Colombo",
            "job_url": "https://example.com",
            "match_score": 92,
            "match_reason": "Strong match on Python and FastAPI",
            "missing_skills": ["Docker", "Kubernetes"]
        }
    ]
    
    send_job_matches("shashika90nuwan@gmail.com", "Shashika", test_jobs)

