import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom"

import Navbar from "./components/Navbar"
import ReportIssue from "./pages/ReportIssue"
import MyReports from "./pages/MyReports"


function App() {
  return (
    <BrowserRouter>

      <div className="min-h-screen bg-slate-950 text-white">

        <Navbar />

        <Routes>

          <Route
            path="/"
            element={<ReportIssue />}
          />

          <Route
            path="/my-reports"
            element={<MyReports />}
          />

        </Routes>

      </div>

    </BrowserRouter>
  )
}


export default App