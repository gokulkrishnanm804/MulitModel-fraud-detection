import { useState } from "react";
import { login, register, setPin, setToken } from "../services/api";

export default function AuthPanel({ onResponse, onToken }) {
  const [email, setEmail] = useState("user1@example.com");
  const [password, setPassword] = useState("Password123");

  const doRegister = async () => {
    const res = await register({
      name: "User One",
      email,
      phone: "9876543210",
      password,
      initial_balance: 10000
    });
    onResponse(res.data);
  };

  const doLogin = async () => {
    const res = await login({ email, password });
    const token = res.data.data.token;
    setToken(token);
    onToken(token);
    onResponse(res.data);
  };

  const doSetPin = async () => {
    const res = await setPin({ pin: "1234", confirm_pin: "1234" });
    onResponse(res.data);
  };

  return (
    <div className="card">
      <h2>Auth</h2>
      <label>Email</label>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <label>Password</label>
      <input value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={doRegister}>Register</button>
      <button onClick={doLogin}>Login</button>
      <button onClick={doSetPin}>Set PIN</button>
      <p className="small">Login stores JWT in runtime memory for API calls.</p>
    </div>
  );
}
