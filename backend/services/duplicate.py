import os
import math

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def get_embedding(text: str):

    if not text:
        return []

    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )

    return response.embeddings[0].values


def cosine_similarity(
    vector_a,
    vector_b
):

    if not vector_a or not vector_b:
        return 0.0

    dot_product = sum(
        a * b
        for a, b in zip(
            vector_a,
            vector_b
        )
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def normalize(value):

    if not value:
        return ""

    return str(value).strip().lower()


def find_best_duplicate(
    description: str,
    category: str,
    location: str,
    reports: list
):

    if not reports:
        return {
            "is_duplicate": False,
            "duplicate_report_id": None,
            "similarity_score": 0.0,
            "duplicate_priority": None
        }

    new_embedding = get_embedding(
        description
    )

    best_report = None
    best_score = 0.0

    new_category = normalize(category)
    new_location = normalize(location)


    for existing in reports:

        existing_text = (
            existing.get(
                "original_description"
            )
            or existing.get("ai_summary")
            or ""
        )

        existing_embedding = get_embedding(
            existing_text
        )

        semantic_score = cosine_similarity(
            new_embedding,
            existing_embedding
        )


        existing_category = normalize(
            existing.get("category")
        )

        existing_location = normalize(
            existing.get(
                "extracted_location"
            )
        )


        category_match = (
            new_category
            and existing_category
            and new_category ==
            existing_category
        )


        location_match = (
            new_location
            and existing_location
            and (
                new_location in existing_location
                or existing_location
                in new_location
            )
        )


        # Start with semantic similarity
        final_score = semantic_score


        # Same category makes duplicate
        # slightly more likely
        if category_match:
            final_score += 0.05


        # Same campus location is a
        # particularly strong signal
        if location_match:
            final_score += 0.10


        final_score = min(
            final_score,
            1.0
        )


        if final_score > best_score:
            best_score = final_score
            best_report = existing


    best_score = round(
        best_score,
        4
    )


    if not best_report:
        return {
            "is_duplicate": False,
            "duplicate_report_id": None,
            "similarity_score": 0.0,
            "duplicate_priority": None
        }


    # Strong semantic match OR
    # slightly weaker semantic match
    # with supporting metadata.
    is_duplicate = (
        best_score >= 0.80
        or (
            best_score >= 0.72
            and (
                normalize(
                    best_report.get(
                        "category"
                    )
                ) == new_category
                or (
                    new_location
                    and normalize(
                        best_report.get(
                            "extracted_location"
                        )
                    ) == new_location
                )
            )
        )
    )


    return {
        "is_duplicate":
            is_duplicate,

        "duplicate_report_id":
            best_report["id"]
            if is_duplicate
            else None,

        "similarity_score":
            best_score,

        "duplicate_priority":
            best_report.get(
                "priority_score"
            )
            if is_duplicate
            else None,

        "is_original":
            is_duplicate
    }