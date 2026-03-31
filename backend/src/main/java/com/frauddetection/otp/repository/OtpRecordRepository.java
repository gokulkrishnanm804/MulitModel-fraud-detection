package com.frauddetection.otp.repository;

import com.frauddetection.otp.entity.OtpRecord;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OtpRecordRepository extends JpaRepository<OtpRecord, Long> {
    Optional<OtpRecord> findTopByUserIdAndTransactionIdOrderByCreatedAtDesc(Long userId, Long transactionId);
}
