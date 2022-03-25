import pandas
from modules.background_tasks.delete_invalid_file.main import get_task_id_from_task_result_file_path

def test_get_task_id_from_task_result_file_path():
    df = pandas.read_csv('src/tests/background_tasks/delete_invalid_file/sample_data/task_file_data.csv')
    print('========================================')

    for i, item in df.iterrows():
        returned_task_id = get_task_id_from_task_result_file_path(item['task_file_name'])
        print(f'test_get_task_id_from_task_result_file_path in Test Case {i}: ', item['task_id'] == returned_task_id)


