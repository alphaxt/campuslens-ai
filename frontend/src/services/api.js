

import { supabase } from "./supabase"

const API_URL = "http://127.0.0.1:8000"


async function getAuthHeaders() {

  const {
    data: { session }
  } = await supabase.auth.getSession()

  if (!session) {
    throw new Error("You must be logged in.")
  }

  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${session.access_token}`
  }
}

export async function createReport(description) {

  const headers = await getAuthHeaders()

  const response = await fetch(
    `${API_URL}/reports`,
    {
      method: "POST",
      headers,
      body: JSON.stringify({
        description
      })
    }
  )

  if (!response.ok) {
    const error = await response.json()

    throw new Error(
      error.detail || "Failed to submit report"
    )
  }

  return response.json()
}

export async function getReports() {

  const headers = await getAuthHeaders()

  const response = await fetch(
    `${API_URL}/reports`,
    {
      headers
    }
  )

  if (!response.ok) {
    const error = await response.json()

    throw new Error(
      error.detail || "Failed to fetch reports"
    )
  }

  return response.json()
}

export async function updateReportStatus(
  reportId,
  status
) {

  const headers = await getAuthHeaders()

  const response = await fetch(
    `${API_URL}/reports/${reportId}/status`,
    {
      method: "PUT",
      headers,
      body: JSON.stringify({
        status
      })
    }
  )

  if (!response.ok) {
    const error = await response.json()

    throw new Error(
      error.detail ||
      "Failed to update report status"
    )
  }

  return response.json()
}


export async function getCampusPulse() {

  const headers = await getAuthHeaders()

  const response = await fetch(
    `${API_URL}/analytics/campus-pulse`,
    {
      headers
    }
  )

  if (!response.ok) {
    const error = await response.json()

    throw new Error(
      error.detail ||
      "Failed to generate Campus Pulse"
    )
  }

  return response.json()
}