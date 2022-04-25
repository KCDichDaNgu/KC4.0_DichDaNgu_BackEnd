# Trong packet này chúng ta sẽ có 3 module chính bao gồm: 
- read_task_result
- mark_invalid_tasks
- execute_in_batch

Hàm main() không có tham số nên chúng ta chỉ xây dựng 1 test case cho hàm main để kiểm tra xem hàm main có chạy hay không

# Cách viết test 
B1: Tải phần mềm hỗ trợ Robo3T về để truy suất những dữ liệu được sử dụng thông qua 
database 

B2: Chạy Backend và FrontEnd, nhớ chạy MongoDB

B3: Khởi động Robo3T, tạo một connection và xem các thuộc tính được sử 
dụng

B4: code và config dữ liệu:

Optional: Sau khi đã quen, chúng ta có thể để dữ liệu theo các trường dữ liệu vào 1 file csv (file data.csv trong code)
để có thể rút ngắn code và run được nhiều test cases hơn.

# Chạy test: Như hướng dẫn ở README ngoài