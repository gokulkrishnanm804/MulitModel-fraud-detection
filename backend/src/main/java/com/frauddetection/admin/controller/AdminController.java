package com.frauddetection.admin.controller;

import com.frauddetection.admin.dto.BlockUserRequest;
import com.frauddetection.admin.dto.DashboardResponse;
import com.frauddetection.admin.service.AdminService;
import com.frauddetection.common.dto.ApiResponse;
import com.frauddetection.transaction.entity.FraudTransaction;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AdminController {

    private final AdminService adminService;

    public AdminController(AdminService adminService) {
        this.adminService = adminService;
    }

    @GetMapping("/dashboard")
    public ApiResponse<DashboardResponse> dashboard() {
        return new ApiResponse<>("Dashboard fetched", adminService.dashboard());
    }

    @GetMapping("/transactions")
    public ApiResponse<List<FraudTransaction>> transactions() {
        return new ApiResponse<>("Transactions fetched", adminService.transactions());
    }

    @PostMapping("/block-user")
    public ApiResponse<String> blockUser(@Valid @RequestBody BlockUserRequest request) {
        adminService.blockUser(request.getUserId(), request.getBlocked());
        return new ApiResponse<>("User status updated", "OK");
    }
}
