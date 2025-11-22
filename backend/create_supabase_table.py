"""
Script to create the appointments table in Supabase.
Run this once to set up the database schema.
"""
import os
import asyncio
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_appointments_table():
    """Create appointments table in Supabase using SQL."""
    
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
        return False
    
    try:
        print("🔌 Connecting to Supabase...")
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # SQL to create the appointments table
        create_table_sql = """
        -- Create appointments table if it doesn't exist
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
        
        -- Create index on email for faster queries
        CREATE INDEX IF NOT EXISTS idx_appointments_email ON appointments(email);
        
        -- Create index on created_at for sorting
        CREATE INDEX IF NOT EXISTS idx_appointments_created_at ON appointments(created_at DESC);
        """
        
        print("📋 Creating appointments table...")
        
        # Execute the SQL using Supabase's rpc function
        # Note: This requires a function to be created in Supabase dashboard first
        # Alternatively, we can use the Supabase dashboard SQL editor to run this
        
        print("✅ Table creation SQL prepared.")
        print("\n" + "="*80)
        print("IMPORTANT: Please run the following SQL in your Supabase SQL Editor:")
        print("="*80)
        print(create_table_sql)
        print("="*80)
        print("\nTo do this:")
        print("1. Go to https://supabase.com/dashboard")
        print("2. Select your project")
        print("3. Go to SQL Editor")
        print("4. Paste the SQL above and click 'Run'")
        print("\n✅ After running the SQL, your appointments table will be ready!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    create_appointments_table()
