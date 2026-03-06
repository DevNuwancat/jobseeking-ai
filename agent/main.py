from supabase import create_client
from dotenv import load_dotenv
from nuwan_colors import Colors, Texts 
from google import genai
import os 

# Load env files 
load_dotenv()

# Connect to Gemini 
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Api connection 
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello in one sentence"
)

# Connect to Supabase 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPERBASE_ANON_KEY")

supabase = create_client(url, key)

# Test connection
print(Colors.green("Supabase Connecting...."))
result = supabase.table("users").select("*").execute()
print("Connected! Users in databse:", len(result.data))

print(response.text)

