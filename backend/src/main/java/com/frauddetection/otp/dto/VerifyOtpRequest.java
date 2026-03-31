package com.frauddetection.otp.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class VerifyOtpRequest {

    @NotNull
    private Long transactionId;

    @NotBlank
    private String otp;

    public Long getTransactionId() { return transactionId; }
    public void setTransactionId(Long transactionId) { this.transactionId = transactionId; }
    public String getOtp() { return otp; }
    public void setOtp(String otp) { this.otp = otp; }
}
