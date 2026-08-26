import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts"


function AnalyticsCharts({ reports = [] }) {
  const categoryData = buildCountData(reports, "category")
  const severityData = buildCountData(reports, "severity")
  const statusData = buildCountData(reports, "status")

  const averagePriority =
    reports.length > 0
      ? Math.round(
          reports.reduce(
            (sum, report) =>
              sum + (Number(report.priority_score) || 0),
            0
          ) / reports.length
        )
      : 0

  const severityColors = [
    "#22c55e",
    "#eab308",
    "#f97316",
    "#ef4444",
    "#64748b",
  ]

  return (
    <div className="space-y-6">

      <div className="grid lg:grid-cols-2 gap-6">

        <ChartCard title="Issues by Category">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={categoryData}>
              <XAxis
                dataKey="name"
                tick={{ fill: "#94a3b8", fontSize: 11 }}
                angle={-20}
                textAnchor="end"
                height={70}
              />

              <YAxis
                allowDecimals={false}
                tick={{ fill: "#94a3b8" }}
              />

              <Tooltip />

              <Bar
                dataKey="value"
                fill="#3b82f6"
                radius={[6, 6, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>


        <ChartCard title="Severity Distribution">
          {severityData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={severityData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={100}
                  label
                >
                  {severityData.map((entry, index) => (
                    <Cell
                      key={entry.name}
                      fill={
                        severityColors[
                          index % severityColors.length
                        ]
                      }
                    />
                  ))}
                </Pie>

                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <EmptyChart />
          )}
        </ChartCard>

      </div>


      <div className="grid lg:grid-cols-2 gap-6">

        <ChartCard title="Reports by Status">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={statusData}>
              <XAxis
                dataKey="name"
                tick={{ fill: "#94a3b8", fontSize: 11 }}
                angle={-20}
                textAnchor="end"
                height={70}
              />

              <YAxis
                allowDecimals={false}
                tick={{ fill: "#94a3b8" }}
              />

              <Tooltip />

              <Bar
                dataKey="value"
                fill="#8b5cf6"
                radius={[6, 6, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>


        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <p className="text-slate-500">
            Average Priority Score
          </p>

          <div className="flex items-end gap-3 mt-4">
            <p className="text-6xl font-bold">
              {averagePriority}
            </p>

            <p className="text-slate-500 mb-2">
              /100
            </p>
          </div>

          <div className="mt-6 h-3 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-500 rounded-full"
              style={{
                width: `${Math.min(
                  Math.max(averagePriority, 0),
                  100
                )}%`,
              }}
            />
          </div>

          <p className="text-sm text-slate-500 mt-4">
            Average calculated priority across all campus reports.
          </p>
        </div>

      </div>

    </div>
  )
}


function ChartCard({ title, children }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
      <h2 className="text-xl font-semibold mb-6">
        {title}
      </h2>

      {children}
    </div>
  )
}


function EmptyChart() {
  return (
    <div className="h-[300px] flex items-center justify-center text-slate-500">
      No report data available.
    </div>
  )
}


function buildCountData(reports, field) {
  const counts = {}

  reports.forEach((report) => {
    const value = report?.[field] || "Unknown"

    counts[value] = (counts[value] || 0) + 1
  })

  return Object.entries(counts).map(
    ([name, value]) => ({
      name,
      value,
    })
  )
}


export default AnalyticsCharts