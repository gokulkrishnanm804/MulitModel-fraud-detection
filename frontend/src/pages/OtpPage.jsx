import { useState } from "react";
import ResultCard from "../components/ResultCard";
import { verifyOtp } from "../services/api";

export default function OtpPage() {
  const [transactionId, setTransactionId] = useState(
    Number(localStorage.getItem("last_tx_id")) || 1
  );
  const [otp, setOtp] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");

  const handleVerify = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const res = await verifyOtp({ transaction_id: Number(transactionId), otp });
      setResponse(res.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "OTP verification failed");
    }
  };

  return (
    <section className="page">
      <div className="card">
        <div className="card-header">
          <h2>OTP verification</h2>
          <p className="muted">Enter the 6-digit OTP to finalize the transaction.</p>
        </div>
        <form className="form" onSubmit={handleVerify}>
          <label>Transaction ID</label>
          <input value={transactionId} onChange={(event) => setTransactionId(event.target.value)} />
          <label>OTP</label>
          <input value={otp} onChange={(event) => setOtp(event.target.value)} />
          {error && <p className="error">{error}</p>}
          <button type="submit">Verify OTP</button>
        </form>
      </div>

      <ResultCard title="Latest Response" data={response} />
    </section>
  );
}
