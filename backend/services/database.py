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

    user_client.auth.set_session(
        access_token=access_token,
        refresh_token=""
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

    user_client.auth.set_session(
        access_token=access_token,
        refresh_token=""
    )

    # Get all reports
    reports_response = (
        user_client
        .table("reports")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    reports = reports_response.data

    # Get all duplicate relationships
    duplicates_response = (
        user_client
        .table("duplicate_relationships")
        .select("report_id, duplicate_of_report_id")
        .execute()
    )

    duplicate_relationships = duplicates_response.data

    # Count duplicate relationships for each report
    duplicate_counts = {}

    for relationship in duplicate_relationships:

        report_id = relationship["report_id"]
        duplicate_of_report_id = relationship["duplicate_of_report_id"]

        duplicate_counts[report_id] = (
            duplicate_counts.get(report_id, 0) + 1
        )

        duplicate_counts[duplicate_of_report_id] = (
            duplicate_counts.get(duplicate_of_report_id, 0) + 1
        )

    # Add duplicate_count to every report
    for report in reports:

        report["duplicate_count"] = duplicate_counts.get(
            report["id"],
            0
        )

    return reports


def get_report_by_id(
    report_id: str,
    access_token: str
):

    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.auth.set_session(
        access_token=access_token,
        refresh_token=""
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

    user_client.auth.set_session(
        access_token=access_token,
        refresh_token=""
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


def add_status_history(
    report_id: str,
    old_status: str,
    new_status: str,
    changed_by: str,
    access_token: str
):
    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.auth.set_session(
        access_token=access_token,
        refresh_token=""
    )

    response = (
        user_client
        .table("status_history")
        .insert({
            "report_id": report_id,
            "old_status": old_status,
            "new_status": new_status,
            "changed_by": changed_by
        })
        .execute()
    )

    return response.data


def get_status_history(
    report_id: str,
    access_token: str
):

    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.auth.set_session(
        access_token=access_token,
        refresh_token=""
    )

    response = (
        user_client
        .table("status_history")
        .select("*")
        .eq("report_id", report_id)
        .order("changed_at")
        .execute()
    )

    return response.data



def get_active_reports(
    access_token: str
):

    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.auth.set_session(
        access_token=access_token,
        refresh_token=""
    )

    response = (
        user_client
        .table("reports")
        .select(
           "id,"
           "original_description,"
           "ai_summary,"
           "category,"
           "extracted_location,"
           "status,"
           "priority_score"
        )
        .execute()
    ) 

    reports = response.data or []

    return [
        report
        for report in reports
        if report.get("status")
        not in ["Resolved", "Closed"]
    ]



def save_duplicate_relationship(
    report_id: str,
    duplicate_of_report_id: str,
    similarity_score: float,
    access_token: str
):

    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.auth.set_session(
        access_token=access_token,
        refresh_token=""
    )

    response = (
        user_client
        .table("duplicate_relationships")
        .insert({
            "report_id": report_id,
            "duplicate_of_report_id":
                duplicate_of_report_id,
            "similarity_score":
                similarity_score
        })
        .execute()
    )

    return response.data


def get_duplicate_count(
    report_id: str,
    access_token: str
):

    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.auth.set_session(
        access_token=access_token,
        refresh_token=""
    )

    response = (
        user_client
        .table("duplicate_relationships")
        .select("count")
        .eq("duplicate_of_report_id", report_id)
        .execute()
    )

    if response and hasattr(response, 'data') and response.data:
        count_data = response.data[0]
        if hasattr(count_data, 'count'):
            return count_data.count
    return 0


def update_report_priority(
    report_id: str,
    new_priority: int,
    access_token: str
):

    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.auth.set_session(
        access_token=access_token,
        refresh_token=""
    )

    response = (
        user_client
        .table("reports")
        .update({
            "priority_score": new_priority
        })
        .eq("id", report_id)
        .execute()
    )

    return response.data


def get_reports_for_priority_update(
    access_token: str
):
    """
    Get all active reports (not Resolved or Closed) that need priority recalculation.
    Used for daily priority recalculation based on duration.
    """
    user_client = create_client(
        supabase_url,
        supabase_key
    )

    user_client.auth.set_session(
        access_token=access_token,
        refresh_token=""
    )

    response = (
        user_client
        .table("reports")
        .select("*")
        .neq("status", "Resolved")
        .neq("status", "Closed")
        .order("created_at", desc=False)
        .execute()
    )

    return response.data