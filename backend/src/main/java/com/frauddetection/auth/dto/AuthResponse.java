package com.frauddetection.auth.dto;

public class AuthResponse {

    private String token;
    private boolean requiresPinSetup;

    public AuthResponse() {
    }

    public AuthResponse(String token, boolean requiresPinSetup) {
        this.token = token;
        this.requiresPinSetup = requiresPinSetup;
    }

    public String getToken() { return token; }
    public void setToken(String token) { this.token = token; }
    public boolean isRequiresPinSetup() { return requiresPinSetup; }
    public void setRequiresPinSetup(boolean requiresPinSetup) { this.requiresPinSetup = requiresPinSetup; }
}
