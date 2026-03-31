package com.frauddetection.transaction.repository;

import com.frauddetection.common.enums.TransactionStatus;
import com.frauddetection.transaction.entity.FraudTransaction;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface FraudTransactionRepository extends JpaRepository<FraudTransaction, Long> {
    long countByStatus(TransactionStatus status);
    List<FraudTransaction> findTop50ByOrderByCreatedAtDesc();
}
