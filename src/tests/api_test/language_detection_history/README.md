Để chạy api test language detection history ta cần làm theo các bước sau:

1. Khởi động backend:
	- Chạy mongodb: `sudo mongod --port 27017 --dbpath /srv/mongodb/db0 --replSet rs0 --bind_ip localhost`
	- (Mở terminal mới) và cd đến backend và nhập các lện sau đây:
		`source .venv/bin/activate`
		`python3 src/server.py run-server -p 8001`
2. Khởi động frontend:
	+ cd vào folder frontend
	+ nhập yarn start vào terminal
3. Thu thập dữ liệu để chuẩn bị chạy api test:
	+ Mở giao diện chương trình chạy trong trình duyệt
	+ Click F12
	+ Đăng nhập với tài khoản dưới đây (hoặc đăng nhập vào google):
		- Tên đăng nhập: admin
		- Mật khẩu: 12345678
	+ Dịch một câu bất kỳ
	+ Trong tab của F12 ta thu thập dữ liệu như sau:
		- Nhấn vào phần get-single trong Name (Chi tiết xem ảnh)
		- Mở preview (có dạng sau):
{
  "taskId": "a5d69b3e-b985-476a-a2d8-c210362638e7",
  "language_detectionType": "public_plain_text_language_detection",
  "id": "1b2f1b66-29ac-4497-86f0-eb1f0c1974ff",
  "status": "detecting",
  "updatedAt": "2022-04-23 15:19:15.584000",
  "createdAt": "2022-04-23 15:19:15.584000",
  "resultUrl": "static/task_result/1650701955571__a5d69b3e-b985-476a-a2d8-c210362638e7.json",
  "posInLangDetectionQueue": 1,
  "estimatedWattingTime": 0.05
}
		- Copy giá trị của taskId và dán vào: `self.x_taskId` trong class estLangDetectionHistoryRequest (Ở hàm khởi tạo)	


		- Cùng một đường dẫn api đó, trỏ con trỏ vào tên của đường dẫn và nhấp chuột trái, di chuyển chuột đến phần Copy/Copy as cURL.
		- Dán phần vừa copy được vào bất kỳ text editor nào để thấy dữ liệu có dạng dưới đây:
		
curl 'http://localhost:8001/lang-detection-history/get-single?taskId=a5d69b3e-b985-476a-a2d8-c210362638e7' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Authorization: 88551f1f-36b6-4517-905c-0bd7435901e8' \
  -H 'Connection: keep-alive' \
  -H 'DNT: 1' \
  -H 'Origin: http://localhost:3000' \
  -H 'Referer: http://localhost:3000/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  --compressed
  
  		- Copy giá trị của 'Authorization' và dán vào `self.x_languageDetectionHistoryId` trong hàm khởi tạo của class TestLangDetectionHistoryRequest.

4. Chạy chương trình bằng cách sử dụng câu lệnh sau trong terminal:
 	`python3 src/tests/api_test/language_detection_history/main.py`
 