package com.frauddetection.fraud.client;

import com.frauddetection.fraud.dto.FraudScoreResult;
import java.util.HashMap;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class FraudMlClient {

    private final RestTemplate restTemplate;
    private final String baseUrl;

    public FraudMlClient(RestTemplate restTemplate, @Value("${fraud.ml.base-url}") String baseUrl) {
        this.restTemplate = restTemplate;
        this.baseUrl = baseUrl;
    }

    public FraudScoreResult score(Map<String, Object> payload) {
        try {
            ResponseEntity<FraudScoreResult> response = restTemplate.postForEntity(
                baseUrl + "/predict",
                payload,
                FraudScoreResult.class);
            if (response.getBody() != null) {
                return response.getBody();
            }
        } catch (Exception ex) {
            // Fall through to safe fallback.
        }

        FraudScoreResult fallback = new FraudScoreResult();
        fallback.setRiskScore(0.5);
        fallback.setRiskLevel("MEDIUM");
        fallback.setReasons(new String[] {"ML service unavailable"});
        return fallback;
    }

    public Map<String, Object> toPayload(int step,
                                         double amount,
                                         double oldOrig,
                                         double newOrig,
                                         double oldDest,
                                         double newDest,
                                         int isNewBeneficiary) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("step", step);
        payload.put("amount", amount);
        payload.put("oldbalanceOrig", oldOrig);
        payload.put("newbalanceOrig", newOrig);
        payload.put("oldbalanceDest", oldDest);
        payload.put("newbalanceDest", newDest);
        payload.put("is_new_beneficiary", isNewBeneficiary);
        return payload;
    }
}
