import { useState } from "react";
import ResultCard from "../components/ResultCard";
import { transfer } from "../services/api";

export default function TransferPage() {
  const [receiverId, setReceiverId] = useState(2);
  const [amount, setAmount] = useState(500);
  const [type, setType] = useState("UPI");
  const [pin, setPin] = useState("1234");
  const [step, setStep] = useState(11);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");

  const handleTransfer = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const res = await transfer({
        receiver_id: Number(receiverId),
        amount: Number(amount),
        type,
        pin,
        step: Number(step)
      });
      setResponse(res.data);
      const txId = res.data?.data?.transaction_id;
      if (txId) {
        localStorage.setItem("last_tx_id", String(txId));
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "Transfer failed");
    }
  };

  return (
    <section className="page">
      <div className="card">
        <div className="card-header">
          <h2>Initiate transfer</h2>
          <p className="muted">Risk engine runs before sending funds.</p>
        </div>
        <form className="form" onSubmit={handleTransfer}>
          <label>Receiver user ID</label>
          <input value={receiverId} onChange={(event) => setReceiverId(event.target.value)} />
          <label>Amount</label>
          <input value={amount} onChange={(event) => setAmount(event.target.value)} />
          <label>Transfer type</label>
          <select value={type} onChange={(event) => setType(event.target.value)}>
            <option value="UPI">UPI</option>
            <option value="CARD">CARD</option>
            <option value="ACCOUNT_TRANSFER">ACCOUNT TRANSFER</option>
          </select>
          <label>Transaction PIN</label>
          <input value={pin} onChange={(event) => setPin(event.target.value)} />
          <label>PaySim step</label>
          <input value={step} onChange={(event) => setStep(event.target.value)} />
          {error && <p className="error">{error}</p>}
          <button type="submit">Send transfer</button>
        </form>
      </div>

      <ResultCard title="Latest Response" data={response} />
    </section>
  );
}
