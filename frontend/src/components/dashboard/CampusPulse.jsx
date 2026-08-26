import { useState } from "react"
import { getCampusPulse } from "../../services/api"


function CampusPulse() {

    const [pulse, setPulse] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")


    async function generatePulse() {

        try {
            setLoading(true)
            setError("")

            const data = await getCampusPulse()

            setPulse(data.pulse)

        } catch (err) {
            setError(err.message)

        } finally {
            setLoading(false)
        }
    }


    return (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">

                <div>

                    <p className="text-blue-400 font-semibold">
                        AI Intelligence
                    </p>

                    <h2 className="text-2xl font-bold mt-1">
                        Campus Pulse
                    </h2>

                    <p className="text-slate-400 mt-2">
                        AI-generated overview of current campus issues and priorities.
                    </p>

                </div>


                <button
                    onClick={generatePulse}
                    disabled={loading}
                    className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 px-5 py-3 rounded-xl font-semibold"
                >
                    {
                        loading
                            ? "Analyzing..."
                            : pulse
                                ? "Refresh Pulse"
                                : "Generate Pulse"
                    }
                </button>

            </div>


            {error && (

                <div className="mt-5 bg-red-950 border border-red-800 text-red-300 p-4 rounded-xl">
                    {error}
                </div>

            )}


            {!pulse && !loading && (

                <div className="mt-6 bg-slate-950 rounded-xl p-6 text-slate-500">
                    Generate Campus Pulse to analyze current report trends.
                </div>

            )}


            {pulse && (

                <div className="mt-7 space-y-6">


                    <div>

                        <p className="text-sm text-slate-500">
                            Current Situation
                        </p>

                        <h3 className="text-2xl font-bold mt-1">
                            {pulse.headline}
                        </h3>

                        <p className="text-slate-300 mt-3 leading-7">
                            {pulse.summary}
                        </p>

                    </div>


                    <div className="grid md:grid-cols-2 gap-4">

                        <PulseItem
                            title="Major Concern"
                            value={pulse.major_concern}
                        />

                        <PulseItem
                            title="Emerging Trend"
                            value={pulse.emerging_trend}
                        />

                        <PulseItem
                            title="Critical Issue"
                            value={pulse.critical_issue}
                        />

                        <PulseItem
                            title="Improvement"
                            value={pulse.improvement}
                        />

                    </div>


                    <div className="bg-slate-950 rounded-xl p-5">

                        <h3 className="font-semibold">
                            Recommended Actions
                        </h3>

                        <div className="mt-4 space-y-3">

                            {
                                pulse.recommended_actions?.map(
                                    (action, index) => (

                                        <div
                                            key={index}
                                            className="flex gap-3"
                                        >

                                            <span className="text-blue-400 font-bold">
                                                {index + 1}.
                                            </span>

                                            <p className="text-slate-300">
                                                {action}
                                            </p>

                                        </div>

                                    )
                                )
                            }

                        </div>

                    </div>

                </div>

            )}

        </div>
    )
}


function PulseItem({ title, value }) {

    return (
        <div className="bg-slate-950 rounded-xl p-5">

            <p className="text-xs uppercase tracking-wide text-slate-500">
                {title}
            </p>

            <p className="mt-2 text-slate-200">
                {value}
            </p>

        </div>
    )
}


export default CampusPulse