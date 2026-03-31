package com.frauddetection.admin.dto;

public class DashboardResponse {

    private long totalTransactions;
    private long fraudCount;
    private long legitCount;
    private long flaggedTransactions;

    public long getTotalTransactions() { return totalTransactions; }
    public void setTotalTransactions(long totalTransactions) { this.totalTransactions = totalTransactions; }
    public long getFraudCount() { return fraudCount; }
    public void setFraudCount(long fraudCount) { this.fraudCount = fraudCount; }
    public long getLegitCount() { return legitCount; }
    public void setLegitCount(long legitCount) { this.legitCount = legitCount; }
    public long getFlaggedTransactions() { return flaggedTransactions; }
    public void setFlaggedTransactions(long flaggedTransactions) { this.flaggedTransactions = flaggedTransactions; }
}
