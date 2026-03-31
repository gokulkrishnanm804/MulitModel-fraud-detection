package com.frauddetection.auth.controller;

import com.frauddetection.auth.dto.AuthResponse;
import com.frauddetection.auth.dto.LoginRequest;
import com.frauddetection.auth.dto.RegisterRequest;
import com.frauddetection.auth.dto.SetPinRequest;
import com.frauddetection.auth.service.AuthService;
import com.frauddetection.common.dto.ApiResponse;
import jakarta.validation.Valid;
import java.security.Principal;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public ApiResponse<AuthResponse> register(@Valid @RequestBody RegisterRequest request) {
        return new ApiResponse<>("User registered", authService.register(request));
    }

    @PostMapping("/login")
    public ApiResponse<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        return new ApiResponse<>("Login success", authService.login(request));
    }

    @PostMapping("/set-pin")
    public ApiResponse<String> setPin(@Valid @RequestBody SetPinRequest request, Principal principal) {
        authService.setPin(principal.getName(), request);
        return new ApiResponse<>("PIN set successfully", "OK");
    }
}
