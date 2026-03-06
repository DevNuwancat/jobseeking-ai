from pypdf import PdfReader
from supabase import create_client
from pypdf.errors import PdfReadError
from google import genai
from dotenv import load_dotenv
from pprint import pprint
from nuwan_colors import Colors, Texts
import json
import os

# Load .env file to Environmet 
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPERBASE_ANON_KEY")

supabase = create_client(url, key)

# Connect to Gemini 
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def parse_pdf(file_path: str) -> str:
    """
    Extract and return all text content from a PDF file.

    Iterates over each page of the PDF and concatenates the extracted text.
    Raises an error if the file is missing, unreadable, or contains no
    machine-readable text (e.g. scanned image PDFs).

    Args:
        file_path (str): Absolute or relative path to the target PDF file.

    Returns:
        str: Concatenated text content extracted from all pages.

    Raises:
        FileNotFoundError: If no file exists at the given path.
        ValueError: If the PDF contains no extractable text (likely a scanned image).
        PdfReadError: If the file is corrupted or not a valid PDF.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        reader = PdfReader(file_path)

        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Guard against PDFs that are image-only (no embedded text layer)
        if not text.strip():
            raise ValueError(
                "PDF contains no extractable text. It may be a scanned image."
            )

        return text

    except PdfReadError:
        raise PdfReadError(f"File is corrupted or not a valid PDF: {file_path}")

def extract_cv_data(text: str) -> str:
    """
    Extract Details for database and retun it as a JSON file
    """
    prompt = f"""
    You are a CV analyzer. Extract information from this CV.
    Return ONLY a JSON object with these exact fields:
    - skills (list of strings)
    - experience_years (number)
    - current_title (string)
    - education (string)
    - languages (list of strings) - Speaking Language 
    - summary (2 sentences max)
    
    CV Text:
    {text}
    
    Return ONLY the JSON, nothing else.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

def save_cv_to_superbase(user_id:str, cv_file_url:str, cv_data:dict) -> None:
    """
    Save extracted CV data to Supabase cv_profile table
    """
    supabase.table("cv_profiles").insert({
        "user_id":user_id,
        "cv_files_url":cv_file_url,
        "skills":cv_data['skills'],
        "experience_years":cv_data['experience_years'],
        "current_title":cv_data['current_title'],
        "education":cv_data['education'],
        "language":cv_data['languages'],
        "summary":cv_data['summary']
    }).execute()

    print(Colors.green("CV saved to Superbase"))


if __name__ == "__main__":
    cv_data = parse_pdf("sample.pdf")
    #print(result)
    result = extract_cv_data(cv_data)

    # Clean the Gemini JSON output 
    clean = result.strip().replace("```json", "").replace("```","")

    # convert string to Python dictionary
    data = json.loads(clean)

    save_cv_to_superbase(
        user_id="107275a8-0fe5-4c3c-bf92-78a17fef7bf6",
        cv_file_url="sample.pdf",
        cv_data=data,
    )
    #pprint(data)
    #print(data['experience_years'])