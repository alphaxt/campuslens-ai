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


def save_report(
    report_data: dict,
    access_token: str
):

    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.postgrest.auth(
        access_token
    )

    response = (
        user_client
        .table("reports")
        .insert(report_data)
        .execute()
    )

    return response.data


def get_all_reports(access_token: str):

    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.postgrest.auth(
        access_token
    )

    response = (
        user_client
        .table("reports")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


def get_report_by_id(
    report_id: str,
    access_token: str
):

    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.postgrest.auth(
        access_token
    )

    response = (
        user_client
        .table("reports")
        .select("*")
        .eq("id", report_id)
        .execute()
    )

    return response.data

def update_report_status(
    report_id: str,
    new_status: str,
    access_token: str
):

    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.postgrest.auth(
        access_token
    )

    response = (
        user_client
        .table("reports")
        .update({
            "status": new_status
        })
        .eq("id", report_id)
        .execute()
    )

    return response.data