import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { supabase } from "../services/supabase"


function Register() {
  const navigate = useNavigate()

  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [message, setMessage] = useState("")


  async function handleSubmit(event) {
    event.preventDefault()

    try {
      setLoading(true)
      setError("")
      setMessage("")

      const { error } =
        await supabase.auth.signUp({
          email,
          password,
          options: {
            data: {
              full_name: fullName
            }
          }
        })

      if (error) {
        throw error
      }

      setMessage(
        "Registration successful. Check your email if confirmation is required."
      )

      setTimeout(() => {
        navigate("/login")
      }, 1500)

    } catch (err) {
      setError(err.message)

    } finally {
      setLoading(false)
    }
  }


  return (
    <div className="min-h-[80vh] flex items-center justify-center px-6">

      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-8">

        <h1 className="text-3xl font-bold">
          Create Account
        </h1>

        <p className="text-slate-400 mt-2">
          Register as a CampusLens student.
        </p>


        <form
          onSubmit={handleSubmit}
          className="mt-8 space-y-5"
        >

          <div>
            <label className="block text-sm text-slate-400 mb-2">
              Full Name
            </label>

            <input
              value={fullName}
              onChange={(event) =>
                setFullName(event.target.value)
              }
              required
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3"
            />
          </div>


          <div>
            <label className="block text-sm text-slate-400 mb-2">
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              required
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3"
            />
          </div>


          <div>
            <label className="block text-sm text-slate-400 mb-2">
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
              minLength="6"
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3"
            />
          </div>


          {error && (
            <p className="text-red-400">
              {error}
            </p>
          )}


          {message && (
            <p className="text-green-400">
              {message}
            </p>
          )}


          <button
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 py-3 rounded-xl font-semibold"
          >
            {
              loading
                ? "Creating account..."
                : "Register"
            }
          </button>

        </form>

      </div>

    </div>
  )
}


export default Register