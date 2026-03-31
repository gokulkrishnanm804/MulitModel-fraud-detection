import { useState } from "react";
import AuthPanel from "./pages/AuthPanel";
import TransactionPanel from "./pages/TransactionPanel";
import AdminPanel from "./pages/AdminPanel";
import ResponseBox from "./components/ResponseBox";

export default function App() {
  const [response, setResponse] = useState(null);
  const [token, setToken] = useState("");

  return (
    <div className="container">
      <h1>Secure Multi-Model Fraud Detection</h1>
      <p className="small">FastAPI backend + ML service + React frontend</p>
      <div className="grid">
        <AuthPanel onResponse={setResponse} onToken={setToken} />
        <TransactionPanel onResponse={setResponse} />
        <AdminPanel onResponse={setResponse} />
        <ResponseBox title="Latest API Response" data={response} />
      </div>
      <p className="small">Token loaded: {token ? "yes" : "no"}</p>
    </div>
  );
}
