import * as React from "react"
import Navigation from "./compound/Navigation"
import "../styles/global.css"

const Layout = ({ children }) => {
  return (
    <>
      <Navigation />
      <main>{children}</main>
      <footer style={{
        textAlign: 'center',
        padding: '2rem',
        marginTop: '4rem',
        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        color: '#94a3b8',
        fontSize: '0.875rem',
      }}>
        © {new Date().getFullYear()} PhishGuard &middot; Protecting users from phishing attacks
      </footer>
    </>
  )
}

export default Layout
