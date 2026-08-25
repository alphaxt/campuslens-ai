import os

from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url:
    raise RuntimeError("SUPABASE_URL is missing from .env")

if not supabase_key:
    raise RuntimeError("SUPABASE_KEY is missing from .env")


supabase: Client = create_client(
    supabase_url,
    supabase_key
)


def save_report(report_data: dict):

    response = (
        supabase
        .table("reports")
        .insert(report_data)
        .execute()
    )

    return response.data