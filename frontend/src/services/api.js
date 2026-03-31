import axios from "axios";

const client = axios.create({
  baseURL: "http://localhost:8080"
});

export const setToken = (token) => {
  if (token) {
    client.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete client.defaults.headers.common.Authorization;
  }
};

export const register = (payload) => client.post("/register", payload);
export const login = (payload) => client.post("/login", payload);
export const setPin = (payload) => client.post("/set-pin", payload);
export const transfer = (payload) => client.post("/transfer", payload);
export const verifyOtp = (payload) => client.post("/verify-otp", payload);
export const dashboard = () => client.get("/dashboard");
export const transactions = () => client.get("/transactions");
export const blockUser = (payload) => client.post("/block-user", payload);
