# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: NhomXX-403
- [REPO_URL]: https://github.com/lehau007/NhomXX-403-Lab13.git
- [MEMBERS]:
  - Member A: Thành viên 1 | Role: Logging & PII
  - Member B: Thành viên 2 | Role: Tracing, SLOs & Alerts (Load Test)
  - Member C: Thành viên 3 | Role: Dashboard, Evidence & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: > 100
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: docs/images/correlation_id.png
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: docs/images/pii_redaction.png
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: docs/images/trace_waterfall.png
- [TRACE_WATERFALL_EXPLANATION]: Trace hiển thị rõ ràng luồng xử lý gồm span RAG retrieval và LLM generation. Có thể thấy rõ bước RAG chiếm phần lớn thời gian (hơn 2.5s) khi bị tiêm sự cố `rag_slow`, giúp khoanh vùng lỗi ngay lập tức mà không cần mò mẫm trong code.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: docs/images/dashboard.png
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 500ms | 28d | *Tự điền lúc chụp Dashboard* |
| Error Rate | < 5% | 28d | *Tự điền lúc chụp Dashboard* |
| Cost Budget | < $2.5/day | 1d | *Tự điền lúc chụp Dashboard* |
| Quality Score | > 0.75 | 28d | *Tự điền lúc chụp Dashboard* |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: docs/images/alert_rules.png
- [SAMPLE_RUNBOOK_LINK]: docs/alerts.md#1-high-latency-p95

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow (Tắc nghẽn hệ thống tìm kiếm tài liệu)
- [SYMPTOMS_OBSERVED]: P95 Latency của toàn hệ thống tăng vọt lên mức > 2500ms, vượt quá xa mốc SLO cho phép (500ms). Dashboard cảnh báo đỏ trên biểu đồ Latency.
- [ROOT_CAUSE_PROVED_BY]: Dựa vào Trace trên Langfuse (xem ảnh Trace Waterfall), thời gian phản hồi của span `retrieve` (hàm RAG) chiếm tới 90% tổng thời gian request (tốn 2.5s), trong khi hàm `generate` (LLM) chỉ tốn ~150ms. Nguyên nhân là do DB Vector bị nghẽn (Timeout/Slow Query).
- [FIX_ACTION]: Tạm thời vô hiệu hóa tính năng tìm kiếm tài liệu để giảm tải (Chạy tính năng RAG Fallback), hoặc tăng cường (Scale up) tài nguyên RAM/CPU cho Vector Database ngay lập tức.
- [PREVENTIVE_MEASURE]: Cài đặt hệ thống Caching (như Redis) để lưu trữ kết quả của các câu truy vấn phổ biến. Bổ sung thêm Rate Limit để tránh hệ thống RAG bị quá tải khi có lượng lớn request (spike) đổ vào cùng lúc. Thiết lập Alert cảnh báo Slack khi RAG latency > 1s.

---

## 5. Individual Contributions & Evidence

### Thành viên 1
- [TASKS_COMPLETED]: Triển khai Correlation ID Middleware, Structured JSON Logging và PII Scrubbing.
- [EVIDENCE_LINK]: (Dán link commit Github vào đây)

### Thành viên 2
- [TASKS_COMPLETED]: Định nghĩa SLOs (`slo.yaml`), thiết lập Alert Rules (`alert_rules.yaml`), chạy kịch bản Load Test và Inject Incidents.
- [EVIDENCE_LINK]: (Dán link commit Github vào đây)

### Thành viên 3
- [TASKS_COMPLETED]: Vẽ 6 biểu đồ Dashboard trên Langfuse, thu thập hình ảnh minh chứng và viết báo cáo RCA.
- [EVIDENCE_LINK]: (Dán link commit Github vào đây)

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Đã đổi từ FakeLLM sang gọi API Gemini 2.0 Flash thực tế, thay đổi cấu trúc bảng giá tính tiền trong `agent.py` để phản ánh đúng chi phí thật (0.075$ input / 0.3$ output).
- [BONUS_AUDIT_LOGS]: N/A
- [BONUS_CUSTOM_METRIC]: N/A
