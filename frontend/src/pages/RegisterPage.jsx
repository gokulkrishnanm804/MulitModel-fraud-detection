import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import ResultCard from "../components/ResultCard";
import { register } from "../services/api";

export default function RegisterPage() {
  const [name, setName] = useState("User One");
  const [email, setEmail] = useState("user1@example.com");
  const [phone, setPhone] = useState("9876543210");
  const [password, setPassword] = useState("Password123");
  const [initialBalance, setInitialBalance] = useState(10000);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const res = await register({
        name,
        email,
        phone,
        password,
        initial_balance: Number(initialBalance)
      });
      setResponse(res.data);
      navigate("/login");
    } catch (err) {
      setError(err?.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <section className="page">
      <div className="card">
        <div className="card-header">
          <h2>Create account</h2>
          <p className="muted">Register and set your transaction PIN after login.</p>
        </div>
        <form className="form" onSubmit={handleRegister}>
          <label>Name</label>
          <input value={name} onChange={(event) => setName(event.target.value)} />
          <label>Email</label>
          <input value={email} onChange={(event) => setEmail(event.target.value)} />
          <label>Phone</label>
          <input value={phone} onChange={(event) => setPhone(event.target.value)} />
          <label>Password</label>
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          <label>Initial balance</label>
          <input value={initialBalance} onChange={(event) => setInitialBalance(event.target.value)} />
          {error && <p className="error">{error}</p>}
          <button type="submit">Register</button>
          <p className="small">
            Already have an account? <Link to="/login">Login</Link>
          </p>
        </form>
      </div>
      <ResultCard title="Latest Response" data={response} />
    </section>
  );
}
