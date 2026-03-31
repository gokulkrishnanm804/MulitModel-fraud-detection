package com.frauddetection.otp.service;

import com.frauddetection.auth.entity.User;
import com.frauddetection.otp.entity.OtpRecord;
import com.frauddetection.otp.repository.OtpRecordRepository;
import java.time.LocalDateTime;
import java.util.Optional;
import java.util.Random;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class OtpService {

    private final OtpRecordRepository otpRecordRepository;
    private final PasswordEncoder passwordEncoder;

    public OtpService(OtpRecordRepository otpRecordRepository, PasswordEncoder passwordEncoder) {
        this.otpRecordRepository = otpRecordRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public void generateOtp(User user, Long transactionId) {
        String otp = String.format("%06d", new Random().nextInt(1000000));

        OtpRecord record = new OtpRecord();
        record.setUser(user);
        record.setOtpHash(passwordEncoder.encode(otp));
        record.setTransactionId(transactionId);
        record.setExpiryTime(LocalDateTime.now().plusMinutes(5));
        record.setUsed(false);
        record.setCreatedAt(LocalDateTime.now());
        otpRecordRepository.save(record);

        // Mock send for development.
        System.out.println("Generated OTP for user " + user.getEmail() + " is: " + otp);
    }

    public boolean verifyOtp(Long userId, Long transactionId, String otp) {
        Optional<OtpRecord> recordOpt = otpRecordRepository.findTopByUserIdAndTransactionIdOrderByCreatedAtDesc(userId, transactionId);
        if (recordOpt.isEmpty()) {
            return false;
        }

        OtpRecord record = recordOpt.get();
        if (record.isUsed() || record.getExpiryTime().isBefore(LocalDateTime.now())) {
            return false;
        }

        boolean valid = passwordEncoder.matches(otp, record.getOtpHash());
        if (valid) {
            record.setUsed(true);
            otpRecordRepository.save(record);
        }

        return valid;
    }
}
