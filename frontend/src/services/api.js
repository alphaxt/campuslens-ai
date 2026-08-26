const API_URL = "http://127.0.0.1:8000"

export async function createReport(description) {
  const response = await fetch(`${API_URL}/reports`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      description,
    }),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Failed to submit report")
  }

  return response.json()
}


export async function getReports() {
  const response = await fetch(`${API_URL}/reports`)

  if (!response.ok) {
    throw new Error("Failed to fetch reports")
  }

  return response.json()
}

export async function updateReportStatus(reportId, status) {
  const response = await fetch(
    `${API_URL}/reports/${reportId}/status`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        status,
      }),
    }
  )

  if (!response.ok) {
    const error = await response.json()
    throw new Error(
      error.detail || "Failed to update report status"
    )
  }

  return response.json()
}


export async function getCampusPulse() {

  const response = await fetch(
    `${API_URL}/analytics/campus-pulse`
  )

  if (!response.ok) {
    const error = await response.json()

    throw new Error(
      error.detail || "Failed to generate Campus Pulse"
    )
  }

  return response.json()
}