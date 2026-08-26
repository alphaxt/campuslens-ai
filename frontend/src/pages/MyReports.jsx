import { useEffect, useState } from "react"
import { getReports } from "../services/api"


function MyReports() {
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")


  useEffect(() => {
    loadReports()
  }, [])


  async function loadReports() {
    try {
      setLoading(true)

      const data = await getReports()

      setReports(data.reports || [])

    } catch (err) {
      setError(err.message)

    } finally {
      setLoading(false)
    }
  }


  if (loading) {
    return (
      <div className="text-center py-20 text-slate-400">
        Loading reports...
      </div>
    )
  }


  return (
    <div className="max-w-6xl mx-auto px-6 py-12">

      <div className="mb-8">
        <p className="text-blue-400 font-semibold">
          CampusLens AI
        </p>

        <h1 className="text-4xl font-bold mt-2">
          My Reports
        </h1>

        <p className="text-slate-400 mt-2">
          View campus issues submitted through the platform.
        </p>
      </div>


      {error && (
        <div className="bg-red-950 border border-red-800 text-red-300 p-4 rounded-xl">
          {error}
        </div>
      )}


      {!error && reports.length === 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-slate-400">
          No reports found.
        </div>
      )}


      <div className="grid gap-4">

        {reports.map((report) => (
          <ReportCard
            key={report.id}
            report={report}
          />
        ))}

      </div>

    </div>
  )
}


function ReportCard({ report }) {

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">

        <div>
          <p className="text-sm text-slate-500">
            {report.id}
          </p>

          <h2 className="text-xl font-semibold mt-1">
            {report.ai_summary}
          </h2>

          <p className="text-slate-400 mt-2">
            {report.original_description}
          </p>
        </div>


        <div className="flex flex-wrap gap-2">

          <SeverityBadge severity={report.severity} />

          <span className="bg-slate-800 px-3 py-1 rounded-full text-sm">
            {report.category}
          </span>

          <span className="bg-slate-800 px-3 py-1 rounded-full text-sm">
            {report.status}
          </span>

        </div>

      </div>


      <div className="mt-5 grid sm:grid-cols-3 gap-4">

        <Info
          label="Location"
          value={report.extracted_location || "Unknown"}
        />

        <Info
          label="Department"
          value={report.recommended_department}
        />

        <Info
          label="Priority"
          value={`${report.priority_score}/100`}
        />

      </div>

    </div>
  )
}


function SeverityBadge({ severity }) {

  const styles = {
    Low: "bg-green-950 text-green-300 border-green-800",
    Medium: "bg-yellow-950 text-yellow-300 border-yellow-800",
    High: "bg-orange-950 text-orange-300 border-orange-800",
    Critical: "bg-red-950 text-red-300 border-red-800",
  }

  return (
    <span
      className={`border px-3 py-1 rounded-full text-sm ${
        styles[severity] || "bg-slate-800"
      }`}
    >
      {severity}
    </span>
  )
}


function Info({ label, value }) {
  return (
    <div className="bg-slate-950 rounded-xl p-4">
      <p className="text-xs text-slate-500 uppercase">
        {label}
      </p>

      <p className="mt-1 font-medium">
        {value}
      </p>
    </div>
  )
}


export default MyReports