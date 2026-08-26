import { Link } from "react-router-dom"

function Navbar() {
  return (
    <nav className="border-b border-slate-800 bg-slate-950">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">

        <Link
          to="/"
          className="text-xl font-bold text-white"
        >
          CampusLens AI
        </Link>

        <div className="flex gap-6 text-sm">
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

          <Link
            to="/admin"
            className="text-slate-300 hover:text-white"
          >
            Admin
          </Link>
        </div>

      </div>
    </nav>
  )
}

export default Navbar