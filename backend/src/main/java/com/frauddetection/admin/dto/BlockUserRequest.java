package com.frauddetection.admin.dto;

import jakarta.validation.constraints.NotNull;

public class BlockUserRequest {

    @NotNull
    private Long userId;

    @NotNull
    private Boolean blocked;

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public Boolean getBlocked() {
        return blocked;
    }

    public void setBlocked(Boolean blocked) {
        this.blocked = blocked;
    }
}
