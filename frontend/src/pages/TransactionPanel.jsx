import { useState } from "react";
import { transfer, verifyOtp } from "../services/api";

export default function TransactionPanel({ onResponse }) {
  const [receiverId, setReceiverId] = useState(2);
  const [amount, setAmount] = useState(100);
  const [otpTxId, setOtpTxId] = useState(1);
  const [otp, setOtp] = useState("000000");

  const doTransfer = async () => {
    const res = await transfer({
      receiver_id: Number(receiverId),
      amount: Number(amount),
      type: "UPI",
      pin: "1234",
      step: 11,
      is_new_beneficiary: 1
    });
    onResponse(res.data);
  };

  const doVerifyOtp = async () => {
    const res = await verifyOtp({ transaction_id: Number(otpTxId), otp });
    onResponse(res.data);
  };

  return (
    <div className="card">
      <h2>Transaction</h2>
      <label>Receiver ID</label>
      <input value={receiverId} onChange={(e) => setReceiverId(e.target.value)} />
      <label>Amount</label>
      <input value={amount} onChange={(e) => setAmount(e.target.value)} />
      <button onClick={doTransfer}>Transfer</button>
      <label>OTP Transaction ID</label>
      <input value={otpTxId} onChange={(e) => setOtpTxId(e.target.value)} />
      <label>OTP</label>
      <input value={otp} onChange={(e) => setOtp(e.target.value)} />
      <button onClick={doVerifyOtp}>Verify OTP</button>
    </div>
  );
}
