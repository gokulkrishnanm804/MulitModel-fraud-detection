package com.frauddetection.admin.service;

import com.frauddetection.admin.dto.DashboardResponse;
import com.frauddetection.auth.entity.User;
import com.frauddetection.auth.repository.UserRepository;
import com.frauddetection.common.enums.TransactionStatus;
import com.frauddetection.transaction.entity.FraudTransaction;
import com.frauddetection.transaction.repository.FraudTransactionRepository;
import java.time.LocalDateTime;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class AdminService {

    private final FraudTransactionRepository transactionRepository;
    private final UserRepository userRepository;

    public AdminService(FraudTransactionRepository transactionRepository, UserRepository userRepository) {
        this.transactionRepository = transactionRepository;
        this.userRepository = userRepository;
    }

    public DashboardResponse dashboard() {
        long total = transactionRepository.count();
        long completed = transactionRepository.countByStatus(TransactionStatus.COMPLETED);
        long flagged = transactionRepository.countByStatus(TransactionStatus.PENDING_OTP)
            + transactionRepository.countByStatus(TransactionStatus.BLOCKED);

        DashboardResponse response = new DashboardResponse();
        response.setTotalTransactions(total);
        response.setFraudCount(flagged);
        response.setLegitCount(completed);
        response.setFlaggedTransactions(flagged);
        return response;
    }

    public List<FraudTransaction> transactions() {
        return transactionRepository.findTop50ByOrderByCreatedAtDesc();
    }

    public void blockUser(Long userId, boolean blocked) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new IllegalArgumentException("User not found"));
        user.setBlocked(blocked);
        user.setUpdatedAt(LocalDateTime.now());
        userRepository.save(user);
    }
}
