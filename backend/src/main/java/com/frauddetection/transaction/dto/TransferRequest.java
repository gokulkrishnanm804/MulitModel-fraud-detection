package com.frauddetection.transaction.dto;

import com.frauddetection.common.enums.TransactionType;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;

public class TransferRequest {

    @NotNull
    private Long receiverId;

    @NotNull
    @DecimalMin(value = "0.01")
    private BigDecimal amount;

    @NotNull
    private TransactionType type;

    @NotNull
    private String pin;

    @NotNull
    private Integer step;

    private Double oldbalanceOrig;
    private Double newbalanceOrig;
    private Double oldbalanceDest;
    private Double newbalanceDest;
    private Integer isNewBeneficiary;

    public Long getReceiverId() { return receiverId; }
    public void setReceiverId(Long receiverId) { this.receiverId = receiverId; }
    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }
    public TransactionType getType() { return type; }
    public void setType(TransactionType type) { this.type = type; }
    public String getPin() { return pin; }
    public void setPin(String pin) { this.pin = pin; }
    public Integer getStep() { return step; }
    public void setStep(Integer step) { this.step = step; }
    public Double getOldbalanceOrig() { return oldbalanceOrig; }
    public void setOldbalanceOrig(Double oldbalanceOrig) { this.oldbalanceOrig = oldbalanceOrig; }
    public Double getNewbalanceOrig() { return newbalanceOrig; }
    public void setNewbalanceOrig(Double newbalanceOrig) { this.newbalanceOrig = newbalanceOrig; }
    public Double getOldbalanceDest() { return oldbalanceDest; }
    public void setOldbalanceDest(Double oldbalanceDest) { this.oldbalanceDest = oldbalanceDest; }
    public Double getNewbalanceDest() { return newbalanceDest; }
    public void setNewbalanceDest(Double newbalanceDest) { this.newbalanceDest = newbalanceDest; }
    public Integer getIsNewBeneficiary() { return isNewBeneficiary; }
    public void setIsNewBeneficiary(Integer isNewBeneficiary) { this.isNewBeneficiary = isNewBeneficiary; }
}
