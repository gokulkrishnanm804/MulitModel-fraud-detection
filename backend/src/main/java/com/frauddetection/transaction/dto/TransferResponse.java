package com.frauddetection.transaction.dto;

public class TransferResponse {

    private Long transactionId;
    private String status;
    private double riskScore;
    private String riskLevel;
    private String message;
    private String[] reasons;

    public Long getTransactionId() { return transactionId; }
    public void setTransactionId(Long transactionId) { this.transactionId = transactionId; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public double getRiskScore() { return riskScore; }
    public void setRiskScore(double riskScore) { this.riskScore = riskScore; }
    public String getRiskLevel() { return riskLevel; }
    public void setRiskLevel(String riskLevel) { this.riskLevel = riskLevel; }
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    public String[] getReasons() { return reasons; }
    public void setReasons(String[] reasons) { this.reasons = reasons; }
}
