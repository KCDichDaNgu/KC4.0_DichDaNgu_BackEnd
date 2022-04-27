## Hướng dẫn cách thực hiện kiểm thử cho hàm `detect_file_language_created_by_public_request`

- Thực hiện cách yêu cầu dịch liên quan đến văn bản
- Vào database và truy cập vào bảng `task` để xem những yêu cầu dịch với trạng thái `not_yet_processed` và tên file là `public_file_language_detection`
- Sao chép phần `task_id`, `created_id` vào file `detect_file_language_data.csv` theo thứ tự `not_yet_processed_task_id`, `created_id`
- Chỉnh sửa file `tests/background_tasks/main.py` phù hợp 
- Thực hiện command `python3 src/server.py run-server -p 8001` để tiến hành quá trình kiểm thử  và quan sát kết quả