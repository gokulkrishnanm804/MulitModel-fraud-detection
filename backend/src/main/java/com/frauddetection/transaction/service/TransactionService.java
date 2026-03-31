package com.frauddetection.transaction.service;

import com.frauddetection.auth.entity.User;
import com.frauddetection.auth.repository.UserRepository;
import com.frauddetection.common.enums.TransactionStatus;
import com.frauddetection.fraud.client.FraudMlClient;
import com.frauddetection.fraud.dto.FraudScoreResult;
import com.frauddetection.otp.dto.VerifyOtpRequest;
import com.frauddetection.otp.service.OtpService;
import com.frauddetection.transaction.dto.TransferRequest;
import com.frauddetection.transaction.dto.TransferResponse;
import com.frauddetection.transaction.entity.FraudTransaction;
import com.frauddetection.transaction.repository.FraudTransactionRepository;
import jakarta.transaction.Transactional;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.Map;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class TransactionService {

    private final UserRepository userRepository;
    private final FraudTransactionRepository transactionRepository;
    private final PasswordEncoder passwordEncoder;
    private final FraudMlClient fraudMlClient;
    private final OtpService otpService;

    public TransactionService(UserRepository userRepository,
                              FraudTransactionRepository transactionRepository,
                              PasswordEncoder passwordEncoder,
                              FraudMlClient fraudMlClient,
                              OtpService otpService) {
        this.userRepository = userRepository;
        this.transactionRepository = transactionRepository;
        this.passwordEncoder = passwordEncoder;
        this.fraudMlClient = fraudMlClient;
        this.otpService = otpService;
    }

    @Transactional
    public TransferResponse transfer(String senderEmail, TransferRequest request) {
        User sender = userRepository.findByEmail(senderEmail)
            .orElseThrow(() -> new IllegalArgumentException("Sender not found"));
        User receiver = userRepository.findById(request.getReceiverId())
            .orElseThrow(() -> new IllegalArgumentException("Receiver not found"));

        if (sender.isBlocked() || receiver.isBlocked()) {
            throw new IllegalArgumentException("Blocked user cannot transact");
        }

        if (sender.getPinHash() == null || !passwordEncoder.matches(request.getPin(), sender.getPinHash())) {
            throw new IllegalArgumentException("Invalid PIN");
        }

        if (sender.getBalance().compareTo(request.getAmount()) < 0) {
            throw new IllegalArgumentException("Insufficient balance");
        }

        Map<String, Object> payload = fraudMlClient.toPayload(
            request.getStep(),
            request.getAmount().doubleValue(),
            request.getOldbalanceOrig() == null ? sender.getBalance().doubleValue() : request.getOldbalanceOrig(),
            request.getNewbalanceOrig() == null ? sender.getBalance().subtract(request.getAmount()).doubleValue() : request.getNewbalanceOrig(),
            request.getOldbalanceDest() == null ? receiver.getBalance().doubleValue() : request.getOldbalanceDest(),
            request.getNewbalanceDest() == null ? receiver.getBalance().add(request.getAmount()).doubleValue() : request.getNewbalanceDest(),
            request.getIsNewBeneficiary() == null ? 0 : request.getIsNewBeneficiary());

        FraudScoreResult score = fraudMlClient.score(payload);

        FraudTransaction tx = new FraudTransaction();
        tx.setSender(sender);
        tx.setReceiver(receiver);
        tx.setAmount(request.getAmount());
        tx.setType(request.getType());
        tx.setRiskScore(BigDecimal.valueOf(score.getRiskScore()));
        tx.setReason(String.join(", ", score.getReasons()));
        tx.setCreatedAt(LocalDateTime.now());
        tx.setUpdatedAt(LocalDateTime.now());

        TransferResponse response = new TransferResponse();
        response.setRiskLevel(score.getRiskLevel());
        response.setRiskScore(score.getRiskScore());
        response.setReasons(score.getReasons());

        if ("LOW".equalsIgnoreCase(score.getRiskLevel())) {
            completeTransfer(tx, sender, receiver);
            response.setTransactionId(tx.getId());
            response.setStatus(tx.getStatus().name());
            response.setMessage("Transaction completed");
            return response;
        }

        tx.setStatus(TransactionStatus.PENDING_OTP);
        FraudTransaction saved = transactionRepository.save(tx);
        otpService.generateOtp(sender, saved.getId());

        response.setTransactionId(saved.getId());
        response.setStatus(saved.getStatus().name());
        response.setMessage("OTP required to complete transaction");
        return response;
    }

    @Transactional
    public TransferResponse verifyOtp(String email, VerifyOtpRequest request) {
        User sender = userRepository.findByEmail(email)
            .orElseThrow(() -> new IllegalArgumentException("User not found"));

        FraudTransaction tx = transactionRepository.findById(request.getTransactionId())
            .orElseThrow(() -> new IllegalArgumentException("Transaction not found"));

        if (!tx.getSender().getId().equals(sender.getId())) {
            throw new IllegalArgumentException("Unauthorized OTP verification");
        }

        if (tx.getStatus() != TransactionStatus.PENDING_OTP) {
            throw new IllegalArgumentException("Transaction is not pending OTP");
        }

        boolean valid = otpService.verifyOtp(sender.getId(), tx.getId(), request.getOtp());
        if (!valid) {
            throw new IllegalArgumentException("Invalid or expired OTP");
        }

        completeTransfer(tx, tx.getSender(), tx.getReceiver());

        TransferResponse response = new TransferResponse();
        response.setTransactionId(tx.getId());
        response.setStatus(tx.getStatus().name());
        response.setRiskScore(tx.getRiskScore().doubleValue());
        response.setRiskLevel(tx.getRiskScore().doubleValue() > 0.7 ? "HIGH" : "MEDIUM");
        response.setMessage("Transaction completed after OTP verification");
        response.setReasons(new String[] {tx.getReason()});
        return response;
    }

    private void completeTransfer(FraudTransaction tx, User sender, User receiver) {
        sender.setBalance(sender.getBalance().subtract(tx.getAmount()));
        receiver.setBalance(receiver.getBalance().add(tx.getAmount()));
        sender.setUpdatedAt(LocalDateTime.now());
        receiver.setUpdatedAt(LocalDateTime.now());
        userRepository.save(sender);
        userRepository.save(receiver);

        tx.setStatus(TransactionStatus.COMPLETED);
        tx.setUpdatedAt(LocalDateTime.now());
        transactionRepository.save(tx);
    }
}
