import os

from fastapi import Header, HTTPException
from supabase import create_client
from fastapi import Depends

from dotenv import load_dotenv


load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_authenticated_user(
    authorization: str = Header(...)
):

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    token = authorization.split(" ", 1)[1]


    client = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )


    try:

        response = client.auth.get_user(token)

        if not response.user:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

        return {
            "id": response.user.id,
            "email": response.user.email,
            "token": token
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )

def require_admin(
    current_user: dict
):

    token = current_user["token"]

    client = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    client.postgrest.auth(token)

    try:
        response = (
            client
            .table("profiles")
            .select("role")
            .eq(
                "id",
                current_user["id"]
            )
            .single()
            .execute()
        )

        profile = response.data

        if not profile:
            raise HTTPException(
                status_code=403,
                detail="Profile not found"
            )

        if profile["role"] != "admin":
            raise HTTPException(
                status_code=403,
                detail="Administrator access required"
            )

        return current_user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=403,
            detail="Unable to verify administrator role"
        )


def get_admin_user(
    current_user: dict = Depends(
        get_authenticated_user
    )
):

    return require_admin(
        current_user
    )