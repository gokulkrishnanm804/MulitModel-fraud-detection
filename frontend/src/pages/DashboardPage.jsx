import { useState } from "react";
import ResultCard from "../components/ResultCard";
import { setPin } from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function DashboardPage() {
  const [pin, setPinValue] = useState("1234");
  const [confirmPin, setConfirmPin] = useState("1234");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");
  const { token } = useAuth();

  const handleSetPin = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const res = await setPin({ pin, confirm_pin: confirmPin });
      setResponse(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to set PIN");
    }
  };

  return (
    <section className="page">
      <div className="card">
        <div className="card-header">
          <h2>Operational overview</h2>
          <p className="muted">Secure transfers, OTP verification, and explainable risk insights.</p>
        </div>
        <div className="grid-slim">
          <div className="stat">
            <p className="eyebrow">JWT loaded</p>
            <h3>{token ? "Active" : "Missing"}</h3>
          </div>
          <div className="stat">
            <p className="eyebrow">Risk tiers</p>
            <h3>LOW / MEDIUM / HIGH</h3>
          </div>
          <div className="stat">
            <p className="eyebrow">OTP policy</p>
            <h3>Required on MEDIUM/HIGH</h3>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h2>Set transaction PIN</h2>
          <p className="muted">Required before your first transfer.</p>
        </div>
        <form className="form" onSubmit={handleSetPin}>
          <label>PIN</label>
          <input value={pin} onChange={(event) => setPinValue(event.target.value)} />
          <label>Confirm PIN</label>
          <input value={confirmPin} onChange={(event) => setConfirmPin(event.target.value)} />
          {error && <p className="error">{error}</p>}
          <button type="submit">Save PIN</button>
        </form>
      </div>

      <ResultCard title="Latest Response" data={response} />
    </section>
  );
}
