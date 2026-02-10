import os
from datetime import datetime, timedelta, timezone
from collections import Counter
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase_key = SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY
supabase: Client = create_client(SUPABASE_URL, supabase_key)

def add_user(user_id: int, item_type: str):
    data = {
        "user_id": user_id,
        "item_type": item_type
    }
    return supabase.table("orders").insert(data).execute()

def get_stats(start, end):
    response = (
        supabase.table("orders")
        .select("item_type")
        .gte("created_at", start.isoformat())
        .lt("created_at", end.isoformat())
        .execute()
    )
    items = [row["item_type"] for row in response.data]
    return Counter(items)

def clear_old(days: int) -> int:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    response = (
        supabase.table("orders")
        .delete()
        .lt("created_at", cutoff.isoformat())
        .execute()
    )
    return len(response.data or [])
