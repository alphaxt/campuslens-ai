import { useState } from "react"
import { createReport } from "../services/api"


function ReportIssue() {
  const [description, setDescription] = useState("")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState("")


  async function handleSubmit(event) {
    event.preventDefault()

    if (!description.trim()) {
      setError("Please describe the campus issue.")
      return
    }

    try {
      setLoading(true)
      setError("")
      setResult(null)

      const data = await createReport(description)

      setResult(data)

    } catch (err) {
      setError(err.message)

    } finally {
      setLoading(false)
    }
  }


  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-3xl mx-auto px-6 py-16">

        <div className="mb-10">
          <p className="text-blue-400 font-semibold">
            CampusLens AI
          </p>

          <h1 className="text-4xl font-bold mt-2">
            Report a Campus Problem
          </h1>

          <p className="text-slate-400 mt-3">
            Describe the problem naturally. AI will classify,
            prioritize and route your report.
          </p>
        </div>


        <form
          onSubmit={handleSubmit}
          className="bg-slate-900 border border-slate-800 rounded-2xl p-6"
        >

          <label className="block font-medium mb-3">
            What happened?
          </label>

          <textarea
            value={description}
            onChange={(event) =>
              setDescription(event.target.value)
            }
            placeholder="Example: Wi-Fi hasn't worked in CS Lab 4 since yesterday."
            rows="7"
            className="w-full bg-slate-950 border border-slate-700 rounded-xl p-4 outline-none focus:border-blue-500"
          />

          {error && (
            <p className="text-red-400 mt-3">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="mt-5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 px-6 py-3 rounded-xl font-semibold"
          >
            {loading ? "AI is analyzing..." : "Analyze & Submit"}
          </button>

        </form>


        {result && (
          <div className="mt-8 bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <h2 className="text-2xl font-bold mb-6">
              AI Analysis
            </h2>

            <div className="grid md:grid-cols-2 gap-4">

              <ResultItem
                label="Summary"
                value={result.analysis.summary}
              />

              <ResultItem
                label="Category"
                value={result.analysis.category}
              />

              <ResultItem
                label="Severity"
                value={result.analysis.severity}
              />

              <ResultItem
                label="Department"
                value={result.analysis.recommended_department}
              />

              <ResultItem
                label="Location"
                value={
                  result.analysis.extracted_location ||
                  "Not detected"
                }
              />

              <ResultItem
                label="Priority Score"
                value={`${result.analysis.priority_score}/100`}
              />

              <ResultItem
                label="Confidence"
                value={`${Math.round(
                  result.analysis.confidence * 100
                )}%`}
              />

            </div>

          </div>
        )}

      </div>
    </div>
  )
}


function ResultItem({ label, value }) {
  return (
    <div className="bg-slate-950 rounded-xl p-4">
      <p className="text-sm text-slate-500">
        {label}
      </p>

      <p className="font-semibold mt-1">
        {value}
      </p>
    </div>
  )
}


export default ReportIssue