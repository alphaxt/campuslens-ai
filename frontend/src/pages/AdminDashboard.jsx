import { useEffect, useMemo, useState } from "react"
import { getReports, updateReportStatus } from "../services/api"
import AnalyticsCharts from "../components/dashboard/AnalyticsCharts"
import CampusPulse from "../components/dashboard/CampusPulse"

function AdminDashboard() {
    const [reports, setReports] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    const [categoryFilter, setCategoryFilter] = useState("All")
    const [severityFilter, setSeverityFilter] = useState("All")
    const [statusFilter, setStatusFilter] = useState("All")


    useEffect(() => {
        loadReports()
    }, [])


    async function loadReports() {
        try {
            setLoading(true)
            setError("")

            const data = await getReports()
            setReports(data.reports || [])

        } catch (err) {
            setError(err.message)

        } finally {
            setLoading(false)
        }
    }


    async function handleStatusChange(
        reportId,
        newStatus
    ) {
        try {
            setError("")

            // Store original status for potential rollback
            const originalReport = reports.find(r => r.id === reportId)
            const originalStatus = originalReport?.status

            // Optimistic update: Update local state immediately
            setReports(prevReports =>
                prevReports.map(report =>
                    report.id === reportId
                        ? { ...report, status: newStatus }
                        : report
                )
            )

            console.log(
                "Optimistic update applied for report",
                reportId,
                "new status:",
                newStatus
            )

            // Call backend to persist the change
            await updateReportStatus(
                reportId,
                newStatus
            )

            console.log(
                "Status update successful for report",
                reportId
            )

        } catch (error) {
            console.error(
                "Failed to update status:",
                error
            )

            // Rollback on error: Revert to original status
            if (originalStatus) {
                setReports(prevReports =>
                    prevReports.map(report =>
                        report.id === reportId
                            ? { ...report, status: originalStatus }
                            : report
                    )
                )
                console.log(
                    "Rollback applied for report",
                    reportId,
                    "restored to:",
                    originalStatus
                )
            }

            setError(error.message)
        }
    }

    const filteredReports = useMemo(() => {
        return reports
            .filter((report) => {

                if (
                    categoryFilter !== "All" &&
                    report.category !== categoryFilter
                ) {
                    return false
                }

                if (
                    severityFilter !== "All" &&
                    report.severity !== severityFilter
                ) {
                    return false
                }

                if (
                    statusFilter !== "All" &&
                    report.status !== statusFilter
                ) {
                    return false
                }

                return true
            })
            .sort(
                (a, b) =>
                    (b.priority_score || 0) -
                    (a.priority_score || 0)
            )

    }, [
        reports,
        categoryFilter,
        severityFilter,
        statusFilter
    ])


    const totalReports = reports.length

    const criticalReports = reports.filter(
        (report) => report.severity === "Critical"
    ).length

    const highPriorityReports = reports.filter(
        (report) =>
            (report.priority_score || 0) >= 70
    ).length

    const resolvedReports = reports.filter(
        (report) => report.status === "Resolved"
    ).length


    if (loading) {
        return (
            <div className="py-20 text-center text-slate-400">
                Loading dashboard...
            </div>
        )
    }


    return (
        <div className="max-w-7xl mx-auto px-6 py-10">

            <div className="mb-10">

                <p className="text-blue-400 font-semibold">
                    Administration
                </p>

                <h1 className="text-4xl font-bold mt-2">
                    Campus Dashboard
                </h1>

                <p className="text-slate-400 mt-2">
                    Monitor campus issues, priorities and resolution activity.
                </p>

            </div>


            {error && (
                <div className="mb-6 bg-red-950 border border-red-800 text-red-300 p-4 rounded-xl">
                    {error}
                </div>
            )}


            {/* Summary Cards */}
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-10">

                <StatCard
                    label="Total Reports"
                    value={totalReports}
                />

                <StatCard
                    label="High Priority"
                    value={highPriorityReports}
                />

                <StatCard
                    label="Critical"
                    value={criticalReports}
                />

                <StatCard
                    label="Resolved"
                    value={resolvedReports}
                />

            </div>


            <div className="mb-10">
                <CampusPulse />
            </div>


            {/* Analytics */}
            <div className="mb-10">
                <AnalyticsCharts reports={reports} />
            </div>


            {/* Filters */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-8">

                <h2 className="text-xl font-semibold mb-5">
                    Filters
                </h2>

                <div className="grid md:grid-cols-3 gap-4">

                    <Filter
                        label="Category"
                        value={categoryFilter}
                        onChange={setCategoryFilter}
                        options={[
                            "All",
                            "Network",
                            "Facilities",
                            "Security",
                            "Cleanliness",
                            "Transport",
                            "Accessibility",
                            "Academic Facilities",
                            "Uncategorized"
                        ]}
                    />

                    <Filter
                        label="Severity"
                        value={severityFilter}
                        onChange={setSeverityFilter}
                        options={[
                            "All",
                            "Low",
                            "Medium",
                            "High",
                            "Critical"
                        ]}
                    />

                    <Filter
                        label="Status"
                        value={statusFilter}
                        onChange={setStatusFilter}
                        options={[
                            "All",
                            "Submitted",
                            "Under Review",
                            "In Progress",
                            "Resolved",
                            "Closed"
                        ]}
                    />

                </div>

            </div>


            {/* Reports Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">

                <div className="p-6 border-b border-slate-800">

                    <div className="flex items-center justify-between gap-4">

                        <div>
                            <h2 className="text-xl font-semibold">
                                Campus Reports
                            </h2>

                            <p className="text-sm text-slate-500 mt-1">
                                {filteredReports.length} reports shown
                            </p>
                        </div>

                        <button
                            onClick={loadReports}
                            className="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg"
                        >
                            Refresh
                        </button>

                    </div>

                </div>


                <div className="overflow-x-auto">

                    <table className="w-full text-left">

                        <thead className="text-sm text-slate-400 border-b border-slate-800">

                            <tr>
                                <th className="p-4">Issue</th>
                                <th className="p-4">Category</th>
                                <th className="p-4">Severity</th>
                                <th className="p-4">Location</th>
                                <th className="p-4">Department</th>
                                <th className="p-4">Priority</th>
                                <th className="p-4">Status</th>
                                <th className="p-4">Duplicates</th>
                            </tr>

                        </thead>


                        <tbody>

                            {filteredReports.map((report) => (

                                <tr
                                    key={report.id}
                                    className="border-b border-slate-800/70 hover:bg-slate-800/40"
                                >

                                    <td className="p-4">

                                        <p className="font-medium max-w-xs">
                                            {report.ai_summary || "No summary"}
                                        </p>

                                        <p className="text-xs text-slate-500 mt-1">
                                            {report.id}
                                        </p>

                                    </td>


                                    <td className="p-4">
                                        {report.category || "Unknown"}
                                    </td>


                                    <td className="p-4">

                                        <SeverityBadge
                                            severity={report.severity}
                                        />

                                    </td>


                                    <td className="p-4">
                                        {report.extracted_location || "Unknown"}
                                    </td>


                                    <td className="p-4">
                                        {report.recommended_department || "Unknown"}
                                    </td>


                                    <td className="p-4">

                                        <PriorityBadge
                                            score={report.priority_score}
                                        />

                                    </td>


                                    <td className="p-4">

                                        <select
                                            value={report.status}
                                            onChange={(event) =>
                                                handleStatusChange(
                                                    report.id,
                                                    event.target.value
                                                )
                                            }
                                            className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-500"
                                        >
                                            <option value="Submitted">
                                                Submitted
                                            </option>

                                            <option value="Under Review">
                                                Under Review
                                            </option>

                                            <option value="In Progress">
                                                In Progress
                                            </option>

                                            <option value="Resolved">
                                                Resolved
                                            </option>

                                            <option value="Closed">
                                                Closed
                                            </option>
                                        </select>

                                    </td>

                                    <td className="p-4">
                                        {report.duplicate_count && report.duplicate_count > 0 ? (
                                            <span className="inline-flex items-center justify-center px-2 py-1 text-xs font-semibold bg-blue-900 text-blue-300 rounded-full border border-blue-700">
                                                {report.duplicate_count} related
                                            </span>
                                        ) : (
                                            <span className="text-xs text-slate-500">None</span>
                                        )}
                                    </td>

                                </tr>

                            ))}

                        </tbody>

                    </table>

                </div>


                {filteredReports.length === 0 && (

                    <div className="p-10 text-center text-slate-500">
                        No reports match the selected filters.
                    </div>

                )}

            </div>

        </div>
    )
}


function StatCard({ label, value }) {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <p className="text-sm text-slate-500">
                {label}
            </p>

            <p className="text-3xl font-bold mt-2">
                {value}
            </p>

        </div>
    )
}


function Filter({
    label,
    value,
    onChange,
    options
}) {
    return (
        <div>

            <label className="block text-sm text-slate-400 mb-2">
                {label}
            </label>

            <select
                value={value}
                onChange={(event) =>
                    onChange(event.target.value)
                }
                className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 outline-none focus:border-blue-500"
            >

                {options.map((option) => (

                    <option
                        key={option}
                        value={option}
                    >
                        {option}
                    </option>

                ))}

            </select>

        </div>
    )
}


function SeverityBadge({ severity }) {

    const styles = {
        Low:
            "bg-green-950 text-green-300 border-green-800",

        Medium:
            "bg-yellow-950 text-yellow-300 border-yellow-800",

        High:
            "bg-orange-950 text-orange-300 border-orange-800",

        Critical:
            "bg-red-950 text-red-300 border-red-800"
    }

    return (
        <span
            className={`inline-block border px-3 py-1 rounded-full text-xs ${styles[severity] ||
                "bg-slate-800 text-slate-300 border-slate-700"
                }`}
        >
            {severity || "Unknown"}
        </span>
    )
}


function PriorityBadge({ score = 0 }) {

    const numericScore = Number(score) || 0

    let style =
        "bg-green-950 text-green-300 border-green-800"

    if (numericScore >= 90) {

        style =
            "bg-red-950 text-red-300 border-red-800"

    } else if (numericScore >= 70) {

        style =
            "bg-orange-950 text-orange-300 border-orange-800"

    } else if (numericScore >= 40) {

        style =
            "bg-yellow-950 text-yellow-300 border-yellow-800"
    }

    return (
        <span
            className={`inline-block border px-3 py-1 rounded-full text-xs font-semibold ${style}`}
        >
            {numericScore}/100
        </span>
    )
}


export default AdminDashboard