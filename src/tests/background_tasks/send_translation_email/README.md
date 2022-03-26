# Module kiểm thử nhóm 13

## Chuẩn bị cho kiểm thử các hàm
Để chuẩn bị cho kiểm thử:

1. Trong /backend/src/infrastructure/configs/main.py, thêm phần sau vào TEST_BACKGROUND_TASKS:
```buildoutcfg
        "test_send_email_result_for_text_translation": BackgroundTask(
            ID="test_send_email_result_for_text_translation",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "test_send_email_result_for_file_translation": BackgroundTask(
            ID="test_send_email_result_for_file_translation",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "test_send_translation_email_main": BackgroundTask(
            ID="test_send_translation_email_main",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        )
```
~2. Trong /backend/src/tests/background_tasks/main.py, thêm các lệnh import ứng với các hàm muốn kiểm thử.

```buildoutcfg
from tests.background_tasks.send_translation_email import <x> as <name>
```
Trong đó, x là:
- **add_fresh_jobs** nếu kiểm thử hàm **send_email_result_for_text_translation**
- **add_fresh_jobs_2** nếu kiểm thử hàm **send_email_result_for_file_translation**
- **add_fresh_jobs_3** nếu kiểm thử hàm **main**

Sau đó, thêm dòng lệnh sau vào cuối file 

```buildoutcfg
new_background_task_scheduler = <name>(new_background_task_scheduler, BACKGROUND_TASKS)
```

**name** là tên mà mình muốn đặt cho hàm.

## Đối với hàm main

1. Sử dụng Robo 3T hoặc các phần mềm cho phép trực quan tương tác với cơ sở dữ liệu.
2. Tại thanh định vị bên trái, chọn translation-tool > Collections > task. 
3. Trong module hiện tại, những task đã chạy được sẽ có trường ```receiver_email``` khác ```null``` và có trường ```total_email_send``` khác ```None``` hoặc ```0```. Ta chuột phát vào các task này, chọn ```Edit Document``` rồi chỉnh giá trị của ```total_email_send``` về ```null``` hoặc ```0``` rồi chạy lại server.

## Đối với các hàm khác

Yêu cầu: Phải có các send_translation_request trong DB.
Các bước tạo:
1. Khởi chạy frontend
2. Trong phần dịch văn bản, sau khi nhập và dịch văn bản, xuất hiện ô nhập địa chỉ email, nhập địa chỉ và gửi.
3. Trong phần dịch tệp, sau khi tải tệp lên và dịch tệp, xuất hiện ô nhập địa chỉ email, nhập địa chỉ và gửi.

Lưu ý: Hàm sẽ sinh test dựa vào các document đã có trong cơ sở dữ liệu. Kết quả chạy test và lý do nếu chạy sai có thể được tìm thấy trong tệp tests cùng thư mục.

## Chạy test

cd vào thư mục backend. Sử dụng lệnh:
```buildoutcfg
python3 src/server.py run-test
```

## Kết quả:

Hàm main không gửi được các email, bị lỗi sau:
```buildoutcfg
501, b'5.5.2 Cannot Decode response i9-20020a17090a2a0900b001c6e540fb6asm6614257pjd.13 - gsmtp'
```

Sau một thời gian chờ đợi, hàm main sẽ bị lỗi sau:
```buildoutcfg
Connection unexpectedly closed
```

Các hàm còn lại không tìm thấy bug.

### UPDATE 1

Cách để kiểm thử hàm main.
1. Sử dụng Robo 3T hoặc một công cụ trực quan cơ sở dữ liệu, ở thanh định vị bên trái, vào translation-tool > Collections > system_setting, thay đổi giá trị của ```email_for_sending_email``` và ```email_password_for_sending_email``` bằng một tài khoản email có thể sử dụng (hãy sử dụng một tài khoản rác) và lưu lại.
2. Vào ```https://myaccount.google.com/security```, tìm kiểm ```Quyền truy cập của ứng dụng kém an toàn```, bật chức năng này.
3. Tìm kiếm ```IMAP enable gmail``` trên trình duyệt, làm theo chỉ dẫn của Microsoft.

Thực hiện tạo test mock như đã hướng dân phần ```Đối với hàm main```.

**KẾT QUẢ**
Giá trị của ```total_email_sent``` tăng lên 1. Chứng tỏ hàm main đã thực hiện đúng chức năng.
