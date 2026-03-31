import { useState } from "react";
import { blockUser, dashboard, transactions } from "../services/api";

export default function AdminPanel({ onResponse }) {
  const [userId, setUserId] = useState(2);
  const [blocked, setBlocked] = useState(false);

  const loadDashboard = async () => {
    const res = await dashboard();
    onResponse(res.data);
  };

  const loadTransactions = async () => {
    const res = await transactions();
    onResponse(res.data);
  };

  const doBlock = async () => {
    const res = await blockUser({ user_id: Number(userId), blocked });
    onResponse(res.data);
  };

  return (
    <div className="card">
      <h2>Admin</h2>
      <button onClick={loadDashboard}>Get Dashboard</button>
      <button onClick={loadTransactions}>Get Transactions</button>
      <label>User ID</label>
      <input value={userId} onChange={(e) => setUserId(e.target.value)} />
      <label>Block user</label>
      <select value={String(blocked)} onChange={(e) => setBlocked(e.target.value === "true")}>
        <option value="false">false</option>
        <option value="true">true</option>
      </select>
      <button onClick={doBlock}>Submit</button>
    </div>
  );
}
