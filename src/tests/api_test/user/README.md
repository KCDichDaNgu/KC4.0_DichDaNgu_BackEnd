Để chạy api test user  ta cần làm theo các bước sau:

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
		- Mở preview và copy giá trị "id" và dán vào `self.x_id` trong hàm khởi tạo của class TestUserGetRequest.
		- Nhấp chuột phải tại me copy/copy as cURL và dán vào text editor (có dạng như sau):
		
curl 'http://localhost:8001/user/me' \
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

		- Copy giá trị của Authorization và dán vào `self.x_access_token` trong hàm khởi tạo của class TestUserGetRequest
		
4. Chạy chương trình bằng cách sử dụng câu lệnh sau trong terminal mới:
 	`python3 src/tests/api_test/user/main.py`

		
