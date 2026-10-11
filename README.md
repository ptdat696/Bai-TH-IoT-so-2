Bài thực hành IoT số 2

1. Giới thiệu

Dự án xây dựng hệ thống giám sát dữ liệu cảm biến IoT, thu thập dữ liệu từ thiết bị ESP32, lưu trữ dữ liệu theo thời gian, tiền xử lý và trực quan hóa kết quả trên dashboard.

Hệ thống sử dụng ESP32 mô phỏng trên Wokwi, ThingsBoard Cloud để tiếp nhận telemetry, InfluxDB để lưu trữ dữ liệu và Python để thu thập, xử lý và hiển thị dữ liệu.

2. Chức năng chính

Thu thập dữ liệu telemetry từ ThingsBoard.

Lưu dữ liệu cảm biến vào InfluxDB.

Tiền xử lý dữ liệu nhiệt độ, độ ẩm và khoảng cách.

Lấy mẫu dữ liệu theo chu kỳ 10 giây.

Phát hiện và xử lý giá trị ngoại lệ bằng phương pháp IQR.

Nội suy một số giá trị bị thiếu và tính trung bình trượt.

Chuẩn hóa dữ liệu về khoảng từ 0 đến 1.

Hiển thị biểu đồ, thông số mới nhất và bảng dữ liệu trên dashboard.

Cho phép tải dữ liệu đã xử lý dưới dạng CSV.

3. Kiến trúc hệ thống

ESP32 / Wokwi
      |
      | Telemetry cảm biến
      v
ThingsBoard Cloud
      |
      | Script thu thập dữ liệu
      v
InfluxDB
      |
      | Truy vấn dữ liệu
      v
Tiền xử lý bằng Python
      |
      v
iot_processed.csv
      |
      v
Streamlit Dashboard

4. Công nghệ sử dụng

Phần cứng mô phỏng: ESP32, Wokwi.

Nền tảng IoT: ThingsBoard Cloud.

Cơ sở dữ liệu chuỗi thời gian: InfluxDB.

Ngôn ngữ: Python.

Thư viện: Requests, InfluxDB Client, Pandas, Streamlit.

Định dạng dữ liệu đầu ra: CSV.

5. Cấu trúc dự án

Bai-TH-IoT-so-2/
├── firmware/             # Mã nguồn ESP32
├── config/               # Cấu hình mẫu
├── database/             # Script database
├── script/
│   ├── collector.py      # Thu thập và ghi dữ liệu
│   ├── preprocess.py     # Tiền xử lý dữ liệu
│   └── dashboard.py      # Dashboard trực quan hóa
├── .env.example          # Mẫu biến môi trường
├── .gitignore
└── README.md

6. Yêu cầu môi trường

Cần cài đặt:

Python 3.10 trở lên.

InfluxDB đang hoạt động và có thể truy cập tại địa chỉ đã cấu hình.

Tài khoản ThingsBoard có quyền truy cập telemetry của thiết bị.

Một database organization và bucket phù hợp trong InfluxDB.

7. Cài đặt

Bước 1: Tải mã nguồn

git clone https://github.com/ptdat696/Bai-TH-IoT-so-2.git
cd Bai-TH-IoT-so-2

Bước 2: Tạo môi trường Python

Trên Windows:

python -m venv .venv
.venv\Scripts\activate

Bước 3: Cài đặt thư viện

pip install requests influxdb-client pandas streamlit

Bước 4: Cấu hình hệ thống

Tạo file .env dựa trên .env.example. Điền các thông tin kết nối ThingsBoard và InfluxDB vào file .env trên máy cá nhân.

Các script cần được sửa để đọc những biến môi trường này. Không đưa mật khẩu hoặc token thật lên GitHub.

8. Hướng dẫn chạy

Bước 1: Thu thập dữ liệu

Tại thư mục gốc dự án, chạy:

python script/collector.py

Script đăng nhập ThingsBoard, truy vấn telemetry và ghi các điểm dữ liệu vào measurement sensor_data trong InfluxDB.

Các trường dữ liệu được thu thập gồm:

temperature: nhiệt độ.

humidity: độ ẩm.

distance_cm: khoảng cách.

rssi: cường độ tín hiệu Wi-Fi.

sequence: số thứ tự bản tin.

uptime_s: thời gian hoạt động của thiết bị.

Script chạy liên tục cho đến khi người dùng dừng bằng Ctrl+C.

Bước 2: Tiền xử lý dữ liệu

Mở một cửa sổ terminal khác, chuyển đến thư mục gốc dự án và chạy:

python script/preprocess.py

Script truy vấn dữ liệu trong một giờ gần nhất từ InfluxDB, sau đó:

Chuyển dữ liệu về dạng bảng theo thời gian.

Lấy mẫu lại theo chu kỳ 10 giây.

Phát hiện ngoại lệ bằng phương pháp IQR.

Nội suy một số giá trị thiếu nằm giữa các điểm dữ liệu.

Tính trung bình trượt với cửa sổ 3 mẫu.

Chuẩn hóa các trường cảm biến về khoảng 0–1.

Xuất kết quả ra file iot_processed.csv tại thư mục làm việc hiện tại.

Bước 3: Khởi chạy dashboard

Sau khi đã tạo file dữ liệu đầu ra, chạy:

streamlit run script/dashboard.py

Mở địa chỉ local do Streamlit hiển thị trong terminal để xem dashboard.

Dashboard cung cấp:

Giá trị nhiệt độ mới nhất.

Giá trị độ ẩm mới nhất.

Giá trị khoảng cách mới nhất.

Biểu đồ biến thiên theo thời gian.

So sánh dữ liệu với trung bình trượt.

Bảng dữ liệu đã tiền xử lý.

Chức năng tải dữ liệu CSV.

Lưu ý: Dashboard cần có file iot_processed.csv. Nếu chưa có dữ liệu, hãy chạy collector và preprocess trước.

9. Kết quả đầu ra

File iot_processed.csv chứa dữ liệu cảm biến đã lấy mẫu, làm sạch và bổ sung các cột trung bình trượt, chuẩn hóa.

Dashboard cho phép theo dõi dữ liệu và tải kết quả phục vụ phân tích, đánh giá thực nghiệm.

Ảnh dashboard và bảng số liệu thực nghiệm sẽ được bổ sung vào báo cáo bàn giao.

10. Bảo mật

Không commit mật khẩu, token hoặc thông tin đăng nhập.

Lưu thông tin bí mật trong file .env cục bộ.

Đưa .env vào .gitignore.

Chỉ đưa file .env.example với giá trị minh họa lên GitHub.

Thu hồi và thay mới các thông tin xác thực đã từng bị đưa lên repo công khai.

11. Hướng phát triển

Bổ sung firmware ESP32 hoàn chỉnh.

Hoàn thiện file cấu hình và tài liệu database.

Bổ sung ảnh dashboard và kết quả thực nghiệm.

Cải thiện xử lý lỗi kết nối và kiểm tra chất lượng dữ liệu.
