# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Nhóm 24
- [REPO_URL]: https://github.com/vinuni/Nhom24-403-lab13
- [MEMBERS]:
  - Ngô Anh Tú | Role: Core Instrumentation (Logging, PII & Tracing)
  - Nguyễn Bá Hào | Role: Reliability & Testing (SLOs, Alerts & Load Test)
  - Lê Văn Hậu | Role: Visualization & Reporting (Dashboard, Evidence & RCA)

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 25
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: ![Correlation ID Log](images/correlation_id_log.png)
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: ![PII Redacted Log](images/pii_redacted_log.png)
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: ![Trace Waterfall](images/langfuse_trace_waterfall.png)
- [TRACE_WATERFALL_EXPLANATION]: Trong hình ảnh trace waterfall của một request chat thành công, span cha `run` tốn khoảng 150ms. Bên trong đó, span con `retrieve` tốn ~10ms và span con `generate` (LLM call) tốn ~140ms. Trace có gắn kèm đầy đủ tags: `lab`, `qa`, `claude-sonnet-4-6` và `user_id`, `session_id`.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: ![Langfuse Dashboard 6 Panels - 1](images/langfuse_dashboard_6_panels_1.png)
- Additional dashboard evidence: ![Langfuse Dashboard 6 Panels - 2](images/langfuse_dashboard_6_panels_2.png)
- Additional dashboard evidence: ![Langfuse Dashboard 6 Panels - 3](images/langfuse_dashboard_6_panels_3.png)
- Additional dashboard evidence: ![Langfuse Dashboard 6 Panels - 4](images/langfuse_dashboard_6_panels_4.png)
- Additional dashboard evidence: ![Langfuse Dashboard 6 Panels - 5](images/langfuse_dashboard_6_panels_5.png)
- Additional dashboard evidence: ![Langfuse Dashboard 6 Panels - 6](images/langfuse_dashboard_6_panels_6.png)
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 185ms |
| Error Rate | < 2% | 28d | 0.0% |
| Cost Budget | < $2.5/day | 1d | $0.05 |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: ![Alert Rules](images/alert_rules.png)
- [SAMPLE_RUNBOOK_LINK]: `docs/alerts.md#HighLatencyAlert`

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: `rag_slow`
- [SYMPTOMS_OBSERVED]: Giao diện Langfuse Dashboard cảnh báo chỉ số "Latency P95" tăng vọt đột biến từ khoảng 200ms lên hơn 2600ms. Đồng thời, metric Request Rate giảm do các request bị treo lâu hơn bình thường, gây nghẽn cục bộ.
- [ROOT_CAUSE_PROVED_BY]: Dựa vào Trace ID `trace-a1b2-c3d4` trên Langfuse, chúng tôi quan sát biểu đồ Waterfall và thấy rằng: span `generate` (gọi LLM) vẫn hoàn thành trong 150ms, nhưng span `retrieve` (truy xuất Vector DB) mất tới 2.5 giây. Log hệ thống cũng ghi nhận thời gian `latency_ms` của API đạt 2650ms mà không báo lỗi 500. Suy ra nguyên nhân gốc rễ là do kết nối từ Agent tới hệ thống RAG/VectorDB bị chậm.
- [FIX_ACTION]: Vô hiệu hóa (disable) sự cố `rag_slow` bằng cách gọi API `/incidents/rag_slow/disable`. Trong thực tế, cần kiểm tra lại tài nguyên của Vector DB, hoặc mở rộng quy mô (scale up).
- [PREVENTIVE_MEASURE]: Thêm cơ chế Timeout (ví dụ 1.0 giây) cho hàm `retrieve()`. Nếu quá 1 giây không lấy được tài liệu thì trả về Fallback (tài liệu rỗng) thay vì làm treo toàn bộ luồng xử lý của hệ thống. Đồng thời cần áp dụng Caching cho những câu truy vấn phổ biến.

---

## 5. Individual Contributions & Evidence

### Ngô Anh Tú
- [TASKS_COMPLETED]: Cấu hình Correlation ID Middleware, gắn context cho Log bằng Structlog, cấu hình regex PII Scrubbing cho Email, SĐT, CCCD; tích hợp thành công Langfuse `@observe()`.
- [EVIDENCE_LINK]: `https://github.com/lehau007/Nhom24-403-Lab13/commit/28e1f7044ccfefe134ecd4c447eb29c0b726210f`

### Nguyễn Bá Hào
- [TASKS_COMPLETED]: Xây dựng Alert Rules, cấu hình file SLO, chạy `load_test.py` với `--concurrency 5` và gọi API `/incidents/rag_slow/enable` để tạo sự cố live.
- [EVIDENCE_LINK]: `https://github.com/lehau007/Nhom24-403-Lab13/commit/391ba75532a7ce97492b4e95daea376a22e95871`

### Lê Văn Hậu
- [TASKS_COMPLETED]: Thiết kế và trích xuất Dashboard 6 panels trên Langfuse/Grafana, thu thập hình ảnh log, phân tích nguyên nhân gốc rễ (RCA) cho sự cố `rag_slow` và viết Blueprint Report.
- [EVIDENCE_LINK]: `https://github.com/lehau007/Nhom24-403-Lab13/commit/f4e24f938e8fee9bd82e563814ba56bea5e31917`

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Không thực hiện (Vẫn dùng Mock LLM)
- [BONUS_AUDIT_LOGS]: Không thực hiện
- [BONUS_CUSTOM_METRIC]: Không thực hiện
