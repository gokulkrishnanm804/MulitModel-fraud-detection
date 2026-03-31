import { useState } from "react";
import ResultCard from "../components/ResultCard";
import {
  adminUsers,
  blockUser,
  fraudLogs,
  fraudTransactions,
  transactions
} from "../services/api";

export default function AdminPage() {
  const [userId, setUserId] = useState(2);
  const [blocked, setBlocked] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");

  const loadUsers = async () => {
    setError("");
    try {
      const res = await adminUsers();
      setResponse(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load users");
    }
  };

  const loadTransactions = async () => {
    setError("");
    try {
      const res = await transactions();
      setResponse(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load transactions");
    }
  };

  const loadFraudTransactions = async () => {
    setError("");
    try {
      const res = await fraudTransactions();
      setResponse(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load fraud transactions");
    }
  };

  const loadFraudLogs = async () => {
    setError("");
    try {
      const res = await fraudLogs();
      setResponse(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load fraud logs");
    }
  };

  const handleBlock = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const res = await blockUser({ user_id: Number(userId), blocked });
      setResponse(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to update user");
    }
  };

  return (
    <section className="page">
      <div className="card">
        <div className="card-header">
          <h2>Admin command center</h2>
          <p className="muted">Monitor flagged activity and manage access.</p>
        </div>
        <div className="button-row">
          <button onClick={loadUsers}>Users</button>
          <button onClick={loadTransactions}>Transactions</button>
          <button onClick={loadFraudTransactions}>Fraud transactions</button>
          <button onClick={loadFraudLogs}>Fraud logs</button>
        </div>
        <form className="form" onSubmit={handleBlock}>
          <label>User ID</label>
          <input value={userId} onChange={(event) => setUserId(event.target.value)} />
          <label>Blocked</label>
          <select value={String(blocked)} onChange={(event) => setBlocked(event.target.value === "true")}>
            <option value="false">false</option>
            <option value="true">true</option>
          </select>
          {error && <p className="error">{error}</p>}
          <button type="submit">Update user</button>
        </form>
      </div>

      <ResultCard title="Latest Response" data={response} />
    </section>
  );
}
