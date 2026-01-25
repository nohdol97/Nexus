import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = __ENV.K6_BASE_URL || "http://localhost:8000";
const API_KEY = __ENV.K6_API_KEY || "dev-key";

export const options = {
  stages: [
    { duration: "30s", target: 20 },
    { duration: "30s", target: 200 },
    { duration: "30s", target: 20 },
    { duration: "30s", target: 0 },
  ],
};

export default function () {
  const url = `${BASE_URL}/v1/chat/completions`;
  const payload = JSON.stringify({
    model: "mock",
    messages: [{ role: "user", content: "spike" }],
  });
  const params = {
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
  };

  const res = http.post(url, payload, params);
  check(res, {
    "status is 200": (r) => r.status === 200,
  });
  sleep(1);
}
