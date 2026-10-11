BÀI THỰC HÀNH SỐ 2

THU THẬP, LƯU TRỮ VÀ TIỀN XỬ LÝ DỮ LIỆU IoT

Học phần: IoT và Ứng dụng (INT14149)
Số tín chỉ:
Thời lượng: 04 tiết thực hành
Đối tượng: Sinh viên đã hoàn thành Bài thực hành số 1
Chuẩn đầu ra: CLO1 (chính), CLO2 (phụ)
1. Mục tiêu
Sau khi hoàn thành bài thực hành, sinh viên có khả năng:
• Xây dựng được pipeline thu thập dữ liệu cảm biến thời gian thực thông qua giao thức MQTT.
• Lựa chọn và triển khai được hệ thống lưu trữ dữ liệu IoT phù hợp (time-series database).
• Thực hiện các bước tiền xử lý dữ liệu thô: làm sạch, phát hiện bất thường, chuẩn hóa và
resampling.
• Phân tích được các vấn đề về lưu trữ, độ trễ và tính toàn vẹn dữ liệu trong hệ thống IoT.
• Xây dựng được dashboard giám sát dữ liệu real-time cơ bản.
2. Yêu cầu tiên quyết
• Đã hoàn thành Bài thực hành số 1 (kết nối thiết bị nhúng, sử dụng MQTT, làm việc với các
nền tảng hỗ trợ IoT).
• Nắm vững kiến thức về cảm biến, giao thức MQTT và mô hình publish/subscribe.
• Có kiến thức cơ bản về Python và xử lý dữ liệu.
3. Nội dung thực hành
3.1. Thu thập dữ liệu IoT
• Cấu hình cảm biến (nhiệt độ, độ ẩm, ánh sáng...) trên thiết bị nhúng (ESP32 / Arduino /
Raspberry Pi).
• Publish dữ liệu theo định dạng JSON lên MQTT Broker với cấu trúc topic chuẩn.
• Xây dựng client thu thập dữ liệu (subscribe) và validate dữ liệu đầu vào.
3.2. Lưu trữ dữ liệu IoT
• Lựa chọn và cài đặt hệ thống cơ sở dữ liệu phù hợp với dữ liệu time-series (InfluxDB khuyến
nghị, hoặc MongoDB Time-Series).
• Thiết kế schema lưu trữ (measurement, tags, fields).
• Ghi dữ liệu real-time từ MQTT vào database.
• Cấu hình retention policy và xử lý dữ liệu trùng lặp / mất mát.
3.3. Tiền xử lý dữ liệu
• Đọc dữ liệu từ database theo khoảng thời gian.
• Xử lý giá trị thiếu (missing values).
• Phát hiện và xử lý outlier (IQR / Z-score).
• Resampling theo cửa sổ thời gian.
• Tạo đặc trưng đơn giản (rolling mean, delta...) và chuẩn hóa dữ liệu.
• Lưu kết quả tiền xử lý vào measurement/collection mới.
3.4. Giám sát và đánh giá
• Xây dựng dashboard hiển thị dữ liệu real-time và dữ liệu đã xử lý.
• Đo và phân tích độ trễ end-to-end của hệ thống.
• Đánh giá các vấn đề về lưu trữ và hiệu năng.
4. Thiết bị và công cụ
4.1. Phần cứng
• Board ESP32 hoặc Arduino + cảm biến (DHT22/BME280, LDR...)
• Raspberry Pi hoặc máy tính đóng vai trò gateway
4.2. Phần mềm
• MQTT Broker: Mosquitto / HiveMQ Cloud / EMQX
• Database: InfluxDB 2.x (khuyến nghị) hoặc MongoDB
• Ngôn ngữ lập trình: Python 3
• Thư viện: paho-mqtt, influxdb-client (hoặc pymongo), pandas, numpy, scikit-learn
• Dashboard: Grafana hoặc Streamlit
• Công cụ hỗ trợ: Docker (khuyến khích)
5. Các bước thực hiện
1. Cấu hình thiết bị nhúng và publish dữ liệu cảm biến lên MQTT Broker theo định dạng JSON
quy định.
2. Xây dựng chương trình client Python subscribe topic, kiểm tra tính hợp lệ của dữ liệu và ghi
vào database.
3. Thiết kế schema database và cấu hình retention policy phù hợp.
4. Viết chương trình tiền xử lý dữ liệu (làm sạch – phát hiện bất thường – resampling – chuẩn
hóa – tạo đặc trưng).
5. Xây dựng dashboard giám sát và thực hiện đo đạc độ trễ, đánh giá hiệu năng lưu trữ.
6. Viết báo cáo và chuẩn bị demo.
6. Sản phẩm cần nộp
1. Mã nguồn (đẩy lên GitHub):
– Firmware thiết bị nhúng
– Script thu thập và ghi dữ liệu
– Script tiền xử lý
– File cấu hình
– File README hướng dẫn chạy rõ ràng
2. Báo cáo (định dạng word, 04–06 trang):
– Sơ đồ kiến trúc hệ thống
– Mô tả schema database
– Kết quả thực nghiệm (ảnh dashboard, bảng số liệu)
– Phân tích độ trễ, vấn đề lưu trữ và đề xuất cải tiến
– Khó khăn và cách giải quyết
3. App ứng dụng.
7. Tiêu chí đánh giá
Tiêu chí Điểm tối đa
Pipeline thu thập và lưu trữ hoạt động ổn định 3.0
Tiền xử lý dữ liệu đúng và có ý nghĩa 2.5
Dashboard và khả năng giám sát real-time 2.0
Chất lượng mã nguồn, xử lý lỗi, tài liệu hướng dẫn 1.5
Báo cáo và phân tích 1.0
Tổng 10.0
8. Ghi chú
• Sinh viên có thể mở rộng thêm edge processing, bảo mật MQTT TLS hoặc so sánh hiệu năng
giữa các loại database.
