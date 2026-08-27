import os

from fastapi import Header, HTTPException
from supabase import create_client

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