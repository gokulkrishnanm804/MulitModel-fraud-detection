package com.frauddetection.auth.service;

import com.frauddetection.auth.dto.AuthResponse;
import com.frauddetection.auth.dto.LoginRequest;
import com.frauddetection.auth.dto.RegisterRequest;
import com.frauddetection.auth.dto.SetPinRequest;
import com.frauddetection.auth.entity.User;
import com.frauddetection.auth.repository.UserRepository;
import java.time.LocalDateTime;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public AuthService(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtService jwtService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    public AuthResponse register(RegisterRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new IllegalArgumentException("Email already exists");
        }
        if (userRepository.existsByPhone(request.getPhone())) {
            throw new IllegalArgumentException("Phone already exists");
        }

        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        user.setPhone(request.getPhone());
        user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
        user.setBalance(request.getInitialBalance());
        user.setBlocked(false);
        user.setRole("USER");
        user.setCreatedAt(LocalDateTime.now());
        user.setUpdatedAt(LocalDateTime.now());

        User saved = userRepository.save(user);
        String token = jwtService.generateToken(saved.getEmail(), saved.getRole());
        return new AuthResponse(token, true);
    }

    public AuthResponse login(LoginRequest request) {
        User user = userRepository.findByEmail(request.getEmail())
            .orElseThrow(() -> new IllegalArgumentException("Invalid credentials"));

        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            throw new IllegalArgumentException("Invalid credentials");
        }

        if (user.isBlocked()) {
            throw new IllegalArgumentException("User is blocked");
        }

        String token = jwtService.generateToken(user.getEmail(), user.getRole());
        return new AuthResponse(token, user.getPinHash() == null);
    }

    public void setPin(String email, SetPinRequest request) {
        if (!request.getPin().equals(request.getConfirmPin())) {
            throw new IllegalArgumentException("PIN and confirm PIN do not match");
        }

        User user = userRepository.findByEmail(email)
            .orElseThrow(() -> new IllegalArgumentException("User not found"));

        user.setPinHash(passwordEncoder.encode(request.getPin()));
        user.setUpdatedAt(LocalDateTime.now());
        userRepository.save(user);
    }
}
