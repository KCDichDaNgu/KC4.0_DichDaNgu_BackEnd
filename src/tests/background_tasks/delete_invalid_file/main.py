import pandas
import os
from datetime import datetime


from modules.background_tasks.delete_invalid_file.main import get_task_id_from_task_result_file_path
from modules.background_tasks.delete_invalid_file.main import get_file_created_time
from modules.background_tasks.delete_invalid_file.main import main
from modules.background_tasks.delete_invalid_file.main import get_to_be_deleted_file_path


def test_get_task_id_from_task_result_file_path():
    df = pandas.read_csv('src/tests/background_tasks/delete_invalid_file/sample_data/task_file_data.csv')
    print('========== DELETE INVALID FILE TEST GET TASK ID FROM TASK RESULT FILE PATH ==========')

    for i, item in df.iterrows():
        returned_task_id = get_task_id_from_task_result_file_path(item['task_file_name'])
        print(f'Test_get_task_id_from_task_result_file_path in Test Case {i}: ', item['task_id'] == returned_task_id)
    
    
def test_get_file_created_time():
    print("========== DELETE INVALID FILE TEST GET FILE CREATED TIME ==========")
    df = pandas.read_csv('src/tests/background_tasks/delete_invalid_file/sample_data/created_time_test.csv')
    for i, item in df.iterrows():
        return_created_file_time = str(get_file_created_time(item['task_file_name']))
        print(f'Test_get_file_created_time in test case {i}: ', item['time']==return_created_file_time)

    
    
def test_get_to_be_deleted_file_path():
    print("========== DELETE INVALID FILE TEST GET TO BE DELETED FILE PATH ==========")
    df = pandas.read_csv('src/tests/background_tasks/delete_invalid_file/sample_data/data.csv')
    for i, item in df.iterrows():
        result = str(get_to_be_deleted_file_path(item['Cases']))
        print(f'Test_get_to_be_deleted_file_path in test case {i}: ', item['Results']==result)

def test_all():
    test_get_task_id_from_task_result_file_path()
    test_get_file_created_time()
    test_get_to_be_deleted_file_path()
