import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout({ children }) {
  const { token, logout } = useAuth();

  return (
    <div className="app-shell">
      <header className="top-bar">
        <div>
          <p className="eyebrow">Explainable AI Fraud Defense</p>
          <h1>Secure Multi-Model Fraud Detection</h1>
        </div>
        <div className="top-actions">
          {token ? (
            <button className="ghost" onClick={logout}>Log out</button>
          ) : (
            <span className="small">Not authenticated</span>
          )}
        </div>
      </header>

      <nav className="nav-links">
        <NavLink to="/dashboard">Dashboard</NavLink>
        <NavLink to="/transfer">Transfer</NavLink>
        <NavLink to="/otp">Verify OTP</NavLink>
        <NavLink to="/admin">Admin</NavLink>
        <span className="spacer" />
        {!token && <NavLink to="/login">Login</NavLink>}
        {!token && <NavLink to="/register">Register</NavLink>}
      </nav>

      <main className="content">{children}</main>
    </div>
  );
}
