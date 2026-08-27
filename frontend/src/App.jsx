import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom"

import ProtectedRoute from "./components/ProtectedRoute"

import Navbar from "./components/Navbar"
import ReportIssue from "./pages/ReportIssue"
import MyReports from "./pages/MyReports"
import AdminDashboard from "./pages/AdminDashboard"
import Login from "./pages/Login"
import Register from "./pages/Register"


function App() {
  return (
    <BrowserRouter>

      <div className="min-h-screen bg-slate-950 text-white">

        <Navbar />

        <Routes>

          <Route
            path="/"
            element={<ProtectedRoute allowedRole="student">
              <ReportIssue />
            </ProtectedRoute>}
          />

          <Route
            path="/my-reports"
            element={<ProtectedRoute allowedRole="student">

              <MyReports />

            </ProtectedRoute>}
          />

          <Route
            path="/admin"
            element={<ProtectedRoute allowedRole="admin">
              <AdminDashboard />
            </ProtectedRoute>}
          />

          <Route
            path="/login"
            element={<Login />}
          />

          <Route
            path="/register"
            element={<Register />}
          />

        </Routes>

      </div>

    </BrowserRouter>
  )
}


export default App