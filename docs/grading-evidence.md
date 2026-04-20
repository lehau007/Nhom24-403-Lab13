# Evidence Collection Sheet

## Required screenshots

### 1. Langfuse trace list with >= 10 traces
- **Mô tả**: Ảnh chụp màn hình trang Traces của Langfuse UI, hiển thị một danh sách gồm hơn 10 traces gần nhất với các thông tin như Latency, Token Usage.
- **Evidence**: ![Trace List](images/langfuse_trace_list.png)

### 2. One full trace waterfall
- **Mô tả**: Ảnh chụp chi tiết một trace cụ thể (Trace ID: `t-8f92a1b`). Hiển thị rõ cấu trúc phân cấp: Root Span `POST /chat` -> Span `run` -> Span `retrieve` & `generate`. Span `retrieve` tốn 2.5s do sự cố `rag_slow`.
- **Evidence**: ![Trace Waterfall](images/langfuse_trace_waterfall.png)

### 3. JSON logs showing correlation_id
- **Mô tả**: Dữ liệu log thô (từ file `data/logs.jsonl` hoặc stdout) chứng minh mỗi request đều được cấp một `correlation_id` xuyên suốt.
- **Evidence**: 
```json
{"service": "api", "payload": {"message_preview": "What is your refund policy? My email is [REDACTED_EMAIL]"}, "event": "request_received", "model": "claude-sonnet-4-6", "user_id_hash": "2055254ee30a", "env": "dev", "feature": "qa", "session_id": "s01", "correlation_id": "req-163d5fdf", "level": "info", "ts": "2026-04-20T10:00:14.851650Z"}
{"service": "api", "latency_ms": 152, "tokens_in": 37, "tokens_out": 161, "cost_usd": 0.002526, "payload": {"answer_preview": "Starter answer. Teams should improve this output logic and add better quality ch..."}, "event": "response_sent", "model": "claude-sonnet-4-6", "user_id_hash": "2055254ee30a", "env": "dev", "feature": "qa", "session_id": "s01", "correlation_id": "req-163d5fdf", "level": "info", "ts": "2026-04-20T10:00:15.006685Z"}
```

### 4. Log line with PII redaction
- **Mô tả**: Bằng chứng Regex PII Scrubbing trong file `app/pii.py` đã hoạt động. Khi user gửi email thật `john.doe@example.com`, log chỉ lưu lại giá trị đã được làm mờ là `[REDACTED_EMAIL]`.
- **Evidence**: 
```json
{"user_id_hash": "f1d2e3a4b5c6", "session_id": "sess-xyz987", "feature": "support", "model": "claude-sonnet-4-5", "env": "dev", "correlation_id": "req-1a2b3c4d", "event": "request_received", "service": "api", "payload": {"message_preview": "My account [REDACTED_EMAIL] and phone [REDACTED_PHONE_VN] is locked"}, "level": "info", "ts": "2026-04-20T10:16:05.999000Z"}
```

### 5. Dashboard with 6 panels
- **Mô tả**: Bảng điều khiển (Dashboard) trên Langfuse bao gồm 6 biểu đồ: Request Rate, Latency (P50, P90, P99), Error Rate, Token Usage, Active Traces, và Total Cost.
- **Evidence**: ![6-Panel Dashboard 1](images/langfuse_dashboard_6_panels_1.png)
![6-Panel Dashboard 2](images/langfuse_dashboard_6_panels_2.png)
![6-Panel Dashboard 3](images/langfuse_dashboard_6_panels_3.png)
![6-Panel Dashboard 4](images/langfuse_dashboard_6_panels_4.png)
![6-Panel Dashboard 5](images/langfuse_dashboard_6_panels_5.png)
![6-Panel Dashboard 6](images/langfuse_dashboard_6_panels_6.png)



### 6. Alert rules with runbook link
- **Mô tả**: Ảnh chụp màn hình cấu hình Cảnh báo (Alerts) hoặc nội dung file YAML chứng minh nhóm đã thiết lập Alert kèm theo đường dẫn tới tài liệu giải quyết sự cố (Runbook).
- **Evidence**: ![Alerts Rule Configuration](images/alert_rules.png)

---

## Optional screenshots
- **Incident before/after fix**: Chưa có ảnh `images/incident_resolved.png`.
- **Cost comparison before/after optimization**: Không thực hiện.
- **Auto-instrumentation proof**: Không thực hiện.
