### How to run test
Testing API **_task_** consists of testing 2 endpoints: 
1. detect-lang: "http://localhost:8001/detect-lang"
    -  Whether the status code in response is 200 (OK) or not: _**test_status_code**_
    - Whether the taskName in response is _public_plain_text_language_detection_ or not: _**test_task_name**_
3. translate: "http://localhost:8001/translate"
    - Whether the status code in response is 200 (OK) or not: _**test_status_code**_
    - Whether the taskName in response is _public_plain_text_translation_ or not: _**test_task_name**_
 
**Command**: 
_$ source .venv/bin/activate_
_$ python3 src/server.py run-server -p 8001_
_$ python3 src/tests/task/main.py_