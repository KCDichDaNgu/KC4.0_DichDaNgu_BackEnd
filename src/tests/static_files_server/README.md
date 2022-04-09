# Testing for static files server from group 13

### Pre-condition:
- Download pseudo-data from: https://drive.google.com/drive/folders/1wwYgMpJNH0fIdNVOixEEr3FWntEq7xa0?usp=sharing
- Extract and copy to KC4.0_DichDaNgu_BackEnd/static


### Testing steps
1. Activate environment: source .venv/bin/activate
2. Install package from requirement.txt: pip install -r src/tests/static_files_server/requirement.txt
3. Run server: python3 src/server.py run-server -p 8001
4. Run code: python3 <full_path_to_static_files_server/main.py> e.g. python3 /home/dangbb/KC4.0_DichDaNgu_BackEnd/src/tests/static_files_server/main.py

### How tests work?

For all request-able files from KC4.0_DichDaNgu_BackEnd/static, main.py will call a request to localhost:8001, get file and save to src/tests/static_files_server/static. In there, main.py will read and extract contents of downloaded file, and the content of corresponding file in KC4.0_DichDaNgu_BackEnd/static, and compare them.

If equals, return true.
Else, identify and log an error.

After compare them, main.py will delete the file.

Also check the status code when request.

All Test got 200.

### Non-OK Test 

Mutated URL, by randomly change a character.
All test got 404.

