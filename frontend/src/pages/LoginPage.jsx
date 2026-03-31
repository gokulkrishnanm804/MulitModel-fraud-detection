import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import ResultCard from "../components/ResultCard";
import { login } from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const [email, setEmail] = useState("user1@example.com");
  const [password, setPassword] = useState("Password123");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");
  const { setToken } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const res = await login({ email, password });
      setResponse(res.data);
      const token = res.data?.data?.token || "";
      if (token) {
        setToken(token);
        navigate("/dashboard");
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed");
    }
  };

  return (
    <section className="page">
      <div className="card">
        <div className="card-header">
          <h2>Welcome back</h2>
          <p className="muted">Authenticate to access transfers and OTP workflow.</p>
        </div>
        <form className="form" onSubmit={handleLogin}>
          <label>Email</label>
          <input value={email} onChange={(event) => setEmail(event.target.value)} />
          <label>Password</label>
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          {error && <p className="error">{error}</p>}
          <button type="submit">Login</button>
          <p className="small">
            New here? <Link to="/register">Create an account</Link>
          </p>
        </form>
      </div>
      <ResultCard title="Latest Response" data={response} />
    </section>
  );
}
