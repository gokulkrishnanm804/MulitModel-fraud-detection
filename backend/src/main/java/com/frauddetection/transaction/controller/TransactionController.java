package com.frauddetection.transaction.controller;

import com.frauddetection.common.dto.ApiResponse;
import com.frauddetection.otp.dto.VerifyOtpRequest;
import com.frauddetection.transaction.dto.TransferRequest;
import com.frauddetection.transaction.dto.TransferResponse;
import com.frauddetection.transaction.service.TransactionService;
import jakarta.validation.Valid;
import java.security.Principal;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TransactionController {

    private final TransactionService transactionService;

    public TransactionController(TransactionService transactionService) {
        this.transactionService = transactionService;
    }

    @PostMapping("/transfer")
    public ApiResponse<TransferResponse> transfer(@Valid @RequestBody TransferRequest request, Principal principal) {
        return new ApiResponse<>("Transfer processed", transactionService.transfer(principal.getName(), request));
    }

    @PostMapping("/verify-otp")
    public ApiResponse<TransferResponse> verifyOtp(@Valid @RequestBody VerifyOtpRequest request, Principal principal) {
        return new ApiResponse<>("OTP verification processed", transactionService.verifyOtp(principal.getName(), request));
    }
}
