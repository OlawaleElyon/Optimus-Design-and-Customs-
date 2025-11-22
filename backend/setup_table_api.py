"""
Script to create appointments table using Supabase REST API.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def create_table_via_api():
    """Create table using direct PostgreSQL connection via Supabase REST API."""
    
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    
    # Try to insert a test record to verify table exists or create it
    # If table doesn't exist, we'll get an error
    
    print("🔌 Attempting to verify/create appointments table...")
    
    # Test if we can query the table
    response = requests.get(
        f"{supabase_url}/rest/v1/appointments?limit=1",
        headers={
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}"
        }
    )
    
    if response.status_code == 200:
        print("✅ Appointments table already exists!")
        return True
    elif "relation" in response.text and "does not exist" in response.text:
        print("❌ Appointments table does not exist.")
        print("\n📝 Please create the table manually using Supabase Dashboard SQL Editor:")
        print("\n" + "="*80)
        print("""
CREATE TABLE IF NOT EXISTS appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    service_type TEXT NOT NULL,
    preferred_date TEXT NOT NULL,
    project_details TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_appointments_email ON appointments(email);
CREATE INDEX IF NOT EXISTS idx_appointments_created_at ON appointments(created_at DESC);
        """)
        print("="*80)
        return False
    else:
        print(f"❌ Error checking table: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    create_table_via_api()
