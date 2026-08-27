import { Navigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"


function ProtectedRoute({
  children,
  allowedRole
}) {

  const {
    user,
    profile,
    loading
  } = useAuth()


  if (loading) {

    return (
      <div className="py-20 text-center text-slate-400">
        Checking authentication...
      </div>
    )
  }


  if (!user) {

    return (
      <Navigate
        to="/login"
        replace
      />
    )
  }


  if (
    allowedRole &&
    profile?.role !== allowedRole
  ) {

    return (
      <Navigate
        to="/"
        replace
      />
    )
  }


  return children
}


export default ProtectedRoute