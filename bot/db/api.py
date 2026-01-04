import os
from collections import Counter
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def add_user(user_id: int, item_type: str):
    data = {
        "user_id": user_id,
        "item_type": item_type
    }
    return supabase.table("orders").insert(data).execute()

def get_stats():
    response = supabase.table("orders").select("item_type").execute()
    items = [row["item_type"] for row in response.data]
    return Counter(items)
