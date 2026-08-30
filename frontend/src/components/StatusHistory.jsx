import { useState, useEffect } from "react"
import { getReportHistory } from "../services/api"


const GEMINI_UNAVAILABLE_MESSAGE =
  "AI analysis is temporarily unavailable. Please try again later."


function StatusHistory({ reportId }) {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")


  useEffect(() => {
    loadHistory()
  }, [reportId])


  async function loadHistory() {
    try {
      setLoading(true)
      setError("")

      const data = await getReportHistory(reportId)

      setHistory(data.history || [])

    } catch (err) {
      // Check if this is a Gemini API failure and replace with user-friendly message
      const errorMessage = err.message.toLowerCase()
      if (
        errorMessage.includes("error") &&
        !errorMessage.includes("failed to")
      ) {
        setError(GEMINI_UNAVAILABLE_MESSAGE)
      } else {
        setError(err.message)
      }

    } finally {
      setLoading(false)
    }
  }


  if (loading) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <p className="text-sm text-slate-400">Loading status history...</p>
      </div>
    )
  }


  if (error) {
    return (
      <div className="bg-red-950 border border-red-800 rounded-xl p-4">
        <p className="text-sm text-red-300">Failed to load history: {error}</p>
      </div>
    )
  }


  if (!history || history.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <p className="text-sm text-slate-500">No status changes yet</p>
      </div>
    )
  }


  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <h3 className="text-sm font-semibold text-slate-300 mb-4">
        Status History
      </h3>

      <div className="space-y-3">
        {history.map((item, index) => (
          <StatusItem
            key={item.id || index}
            item={item}
          />
        ))}
      </div>
    </div>
  )
}


function StatusItem({ item }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
      hour12: true
    })
  }


  return (
    <div className="flex items-center gap-3 text-sm">
      <div className="flex-shrink-0 w-1.5 h-1.5 rounded-full bg-slate-600" />
      <div className="flex-1 min-w-0">
        <p className="text-slate-400">
          Status changed from <span className="text-slate-300 font-medium">
            {item.old_status || "N/A"}
          </span> to <span className="text-slate-300 font-medium">
            {item.new_status || "N/A"}
          </span>
        </p>
        <p className="text-xs text-slate-500 mt-0.5">
          {formatDate(item.changed_at)}
        </p>
      </div>
    </div>
  )
}


export default StatusHistory
