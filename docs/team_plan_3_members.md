
# Kế hoạch thực hiện Lab 13 (Dành cho nhóm 3 thành viên)

Do nhóm chỉ có 3 thành viên (thay vì 6 như gợi ý ban đầu), khối lượng công việc sẽ được gom nhóm lại thành 3 mảng chính: **Lõi Hệ thống (Core)**, **Đảm bảo Chất lượng (Reliability)**, và **Báo cáo & Trình bày (Reporting)**.

## 1. Phân công công việc (Role Assignment)

### 🧑‍💻 Thành viên 1: Core Instrumentation (Logging, PII & Tracing)
Chịu trách nhiệm thiết lập các nền tảng quan sát cốt lõi cho ứng dụng FastAPI.
*   **Nhiệm vụ:**
    *   Tạo Correlation IDs cho mỗi request.
    *   Làm giàu cấu trúc log (JSON structured logging) với các context như user, session.
    *   Viết logic ẩn thông tin nhạy cảm (PII Scrubbing).
    *   Tích hợp Langfuse Tracing để theo dõi luồng thực thi (traces).
*   **Mục tiêu hoàn thành:** Chạy `python scripts/validate_logs.py` không báo lỗi & Langfuse ghi nhận được tối thiểu 10 traces.

### 🕵️ Thành viên 2: Reliability & Testing (SLOs, Alerts & Load/Failure Testing)
Chịu trách nhiệm định nghĩa tiêu chuẩn, thiết lập cảnh báo và mô phỏng các tình huống thực tế/sự cố.
*   **Nhiệm vụ:**
    *   Thiết lập Service Level Objectives (SLOs) trong config.
    *   Thiết lập Alert rules (Cảnh báo) để phát hiện sự cố.
    *   Chạy công cụ tạo tải ảo (Load test) để mô phỏng traffic.
    *   Cố tình tạo ra sự cố (Inject incident) để kiểm tra xem hệ thống cảnh báo và tracing có hoạt động đúng không.
*   **Mục tiêu hoàn thành:** Hệ thống có sinh ra logs lỗi thực tế, kích hoạt được các trigger cảnh báo dựa trên luật đã viết.

### 📊 Thành viên 3: Visualization & Reporting (Dashboard, Evidence & Demo)
Chịu trách nhiệm trực quan hóa dữ liệu, tổng hợp minh chứng và chuẩn bị tài liệu nộp bài.
*   **Nhiệm vụ:**
    *   Thu thập metrics và xây dựng Dashboard gồm đủ 6 biểu đồ (panels).
    *   Viết báo cáo RCA (Root Cause Analysis - Phân tích nguyên nhân gốc rễ) từ các sự cố do Thành viên 2 tạo ra.
    *   Điền đầy đủ thông tin vào các file tài liệu nộp bài.
    *   Chuẩn bị kịch bản và dẫn dắt phần Demo cho giảng viên.
*   **Mục tiêu hoàn thành:** Hoàn thiện `blueprint-template.md`, `grading-evidence.md` và Dashboard có dữ liệu realtime.

---

## 2. Quy trình phối hợp nhóm (Workflow)

Để đảm bảo không bị conflict code và các thành viên có dữ liệu để làm việc, nhóm cần tuân thủ thứ tự sau:

1.  **Giai đoạn 1 (Cùng nhau): Khởi tạo**
    *   Cả nhóm clone code, cài đặt môi trường ảo (venv), cài thư viện từ `requirements.txt`.
    *   Copy `.env.example` sang `.env` và điền các API Key cần thiết (ví dụ: Langfuse keys).
2.  **Giai đoạn 2 (Thành viên 1 đi trước 1 bước): Cài đặt Core**
    *   Thành viên 1 phải hoàn thiện Logging và Tracing trước để có dữ liệu chuẩn. Thành viên 2 và 3 có thể bắt đầu đọc tài liệu (`docs/`) và draft các file cấu hình yaml/json.
3.  **Giai đoạn 3 (Thành viên 2 tạo dữ liệu): Mô phỏng**
    *   Khi code của Thành viên 1 đã push, Thành viên 2 kéo (pull) về và bắt đầu chạy `load_test.py` và `inject_incident.py` để đẩy hàng loạt log, traces và metrics hệ thống.
4.  **Giai đoạn 4 (Thành viên 3 tổng hợp): Trực quan hóa**
    *   Thành viên 3 dựa trên dữ liệu thật đang được tạo ra bởi Thành viên 2 để cấu hình Dashboard và chụp ảnh màn hình (evidence). Cùng lúc đó, cả nhóm phối hợp để viết báo cáo sự cố (RCA).
5.  **Giai đoạn 5: Review & Demo**
    *   Gộp toàn bộ code, chạy thử quy trình từ đầu đến cuối nghiệm thu chéo các `TODO`.
