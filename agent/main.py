from supabase import create_client
from dotenv import load_dotenv
from nuwan_colors import Colors, Texts 
import os 

# Load env files 
load_dotenv()

# Connect to Supabase 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPERBASE_ANON_KEY")

supabase = create_client(url, key)

# Test connection
print(Colors.green("Supabase Connecting...."))
result = supabase.table("users").select("*").execute()
print("Connected! Users in databse:", len(result.data))

