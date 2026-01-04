import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def add_user(user_id: int, item_type: str):
    data = {
        'user_id': user_id,
        'item_type': item_type
    }
    response = supabase.table('orders').insert(data).execute()
    return response