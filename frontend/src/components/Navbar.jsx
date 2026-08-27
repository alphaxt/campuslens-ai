import {
  Link,
  useNavigate
} from "react-router-dom"

import { useAuth } from "../context/AuthContext"


function Navbar() {

  const navigate = useNavigate()

  const {
    user,
    profile,
    loading,
    signOut
  } = useAuth()


  async function handleSignOut() {

    await signOut()

    navigate("/login")
  }


  return (
    <nav className="border-b border-slate-800 bg-slate-950">

      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">

        <Link
          to="/"
          className="text-xl font-bold text-white"
        >
          CampusLens AI
        </Link>


        <div className="flex items-center gap-6 text-sm">

          {!loading && !user && (
            <>
              <Link
                to="/"
                className="text-slate-300 hover:text-white"
              >
                Report Issue
              </Link>

              <Link
                to="/login"
                className="text-slate-300 hover:text-white"
              >
                Login
              </Link>

              <Link
                to="/register"
                className="text-slate-300 hover:text-white"
              >
                Register
              </Link>
            </>
          )}


          {!loading &&
            user &&
            profile?.role === "student" && (
              <>
                <Link
                  to="/"
                  className="text-slate-300 hover:text-white"
                >
                  Report Issue
                </Link>

                <Link
                  to="/my-reports"
                  className="text-slate-300 hover:text-white"
                >
                  My Reports
                </Link>
              </>
            )}


          {!loading &&
            user &&
            profile?.role === "admin" && (
              <>
                <Link
                  to="/admin"
                  className="text-slate-300 hover:text-white"
                >
                  Admin Dashboard
                </Link>
              </>
            )}


          {!loading && user && (
            <>
              <div className="hidden md:block text-slate-400">

                {profile?.full_name ||
                  user.email}

                <span className="ml-2 text-xs text-blue-400">
                  {profile?.role}
                </span>

              </div>


              <button
                onClick={handleSignOut}
                className="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg"
              >
                Sign Out
              </button>
            </>
          )}

        </div>

      </div>

    </nav>
  )
}


export default Navbar