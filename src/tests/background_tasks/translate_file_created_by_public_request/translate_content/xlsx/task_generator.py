import json
import os
import requests
import time

HOST = 'http://localhost'
BACKEND_PORT = 8001
MAX_RETRIES = 5

# Create a new detection task by making request to backend


def create_detection_task(file_path: str):
    # Read file
    files = {'file': open(file_path, 'r')}

    # Create request
    response = requests.post(
        f'{HOST}:{BACKEND_PORT}/detect-f-lang', files=files)

    # Parsing response and return the data
    data = json.loads(response.text)['data']
    return data


# Get language detection result from backend
def detect_language(file_path: str):
    # Get task details
    task = create_detection_task(file_path)

    # Get detected language
    url = f'{HOST}:{BACKEND_PORT}/lang-detection-history/get-single?taskId={task["taskId"]}'
    retries = 0
    while(True):
        if retries >= MAX_RETRIES:
            print('Max retries reached, terminating detect_language...')
            break
        retries += 1
        time.sleep(1)
        response = requests.get(url)
        data = json.loads(response.text)['data']
        if data['status'] == 'detecting':
            continue
        else:
            result_url = data['resultUrl']
            url = f'{HOST}:{BACKEND_PORT}/{result_url}'
            response = requests.get(url)
            data = json.loads(response.text)
            return data


# Create a new translation task by making request to backend
def create_translation_task(file_path: str):
    # Get language detection result
    detection_result = detect_language(file_path)

    # Read file
    files = {'file': open(file_path, 'r')}

    # Source language and target language
    src = detection_result['source_lang']
    dst = 'vi'

    # Create request
    response = requests.post(
        f'{HOST}:{BACKEND_PORT}/translate_f',
        data={
            'sourceLang': src,
            'targetLang': dst
        },
        files=files
    )

    # Parsing response and return the data
    data = json.loads(response.text)['data']
    return data


# Translate a file
def translate(file_path: str):
    # Get task details
    task = create_translation_task(file_path)

    # Get translation result
    url = f'http://localhost:8001/translation-history/get-single'
    url = f'{url}?translationHistoryId={task["translationHitoryId"]}'
    url = f'{url}&taskId={task["taskId"]}'
    retries = 0
    while(True):
        if retries >= MAX_RETRIES:
            print('Max retries reached, terminating translate...')
            return None
        retries += 1
        time.sleep(1)
        response = requests.get(url)
        data = json.loads(response.text)['data']
        if data['status'] == 'translating':
            continue
        else:
            result_url = data['resultUrl']
            url = f'{HOST}:{BACKEND_PORT}/{result_url}'
            response = requests.get(url)
            data = json.loads(response.text)
            return data


# Generate translation tasks from testcases
def generate_tasks(test_dir: str):
    try:
        # Get all files in test_dir
        files = [f for f in os.listdir(
            test_dir) if os.path.isfile(os.path.join(test_dir, f))]

        print(f'{len(files)} testcases found:\n|')
        for file in files:
            print(f'\--{file}')

        # Create tasks
        for file in files:
            print(f'Processing {file}')
            result = translate(os.path.join(test_dir, file))
            if result is None:
                print(f'Failed to translate {file}')
            else:
                print(f'{file} translated')

        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    generate_tasks('../test_files') 