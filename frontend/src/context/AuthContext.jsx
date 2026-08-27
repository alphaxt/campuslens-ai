import {
  createContext,
  useContext,
  useEffect,
  useState
} from "react"

import { supabase } from "../services/supabase"


const AuthContext = createContext(null)


export function AuthProvider({ children }) {

  const [user, setUser] = useState(null)
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)


  async function loadProfile(currentUser) {

    if (!currentUser) {
      setProfile(null)
      return
    }

    const { data, error } = await supabase
      .from("profiles")
      .select("*")
      .eq("id", currentUser.id)
      .single()

    if (error) {
      console.error(
        "Profile loading failed:",
        error
      )

      setProfile(null)
      return
    }

    setProfile(data)
  }


  async function loadSession() {

    const {
      data: { session }
    } = await supabase.auth.getSession()

    const currentUser =
      session?.user || null

    setUser(currentUser)

    await loadProfile(currentUser)

    setLoading(false)
  }


  useEffect(() => {

    loadSession()


    const {
      data: { subscription }
    } = supabase.auth.onAuthStateChange(
      async (_event, session) => {

        const currentUser =
          session?.user || null

        setUser(currentUser)

        await loadProfile(currentUser)

        setLoading(false)
      }
    )


    return () => {
      subscription.unsubscribe()
    }

  }, [])


  async function signOut() {

    await supabase.auth.signOut()

    setUser(null)
    setProfile(null)
  }


  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        loading,
        signOut
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}


export function useAuth() {

  return useContext(AuthContext)
}