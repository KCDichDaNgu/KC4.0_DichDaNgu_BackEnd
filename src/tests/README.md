*Môi trường: Ubuntu 20.04*

### Nơi thực hiện viết các ca kiểm thử

``` sh
#/backend/src/tests
```

### Nơi thêm mới cấu hình cho các background tasks mới

``` sh
#/backend/src/infrastructure/configs/main.py#TEST_BACKGROUND_TASKS
```

### Thêm các thư viện cần dùng trong quá trình kiểm thử

``` sh
#/backend/src/tests/test_requirements.txt
```

### Cài đặt các thư viện

``` sh
#/backend/
$ pip install -r src/tests/test_requirements.txt
```

### Khởi chạy các ca kiểm thử

``` sh
#/backend/
$ python3 src/server.py run-test -p 8001
```