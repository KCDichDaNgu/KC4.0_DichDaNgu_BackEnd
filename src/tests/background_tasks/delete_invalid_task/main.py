import pandas


from modules.background_tasks.delete_invalid_task.main import get_task_id_from_task_result_file_path
from modules.background_tasks.delete_invalid_task.main import main
from modules.background_tasks.delete_invalid_task.main import get_to_be_deleted_file_path


def test_get_task_id_from_task_result_file_path_delete_invalid_task():
    df = pandas.read_csv('src/tests/background_tasks/delete_invalid_task/sample_data/task_file_data.csv')
    print('========== DELETE INVALID TASK TEST GET TASK ID FROM TASK RESULT FILE PATH ==========')

    for i, item in df.iterrows():
        returned_task_id = get_task_id_from_task_result_file_path(item['task_file_name'])
        print(f'Test_get_task_id_from_task_result_file_path in Test Case {i}: ', item['task_id'] == returned_task_id)
    
        
    
def test_get_to_be_deleted_file_path_delete_invalid_task():
    print("========== DELETE INVALID TASK TEST GET TO BE DELETED FILE PATH ==========")
    df = pandas.read_csv('src/tests/background_tasks/delete_invalid_task/sample_data/data.csv')
    for i, item in df.iterrows():
        result = str(test_get_to_be_deleted_file_path_delete_invalid_task(item['Cases']))
        print(f'Test_get_to_be_deleted_file_path in test case {i}: ', item['Results']==result)    

async def test_main_delete_invalid_task():
    print('========== DELETE INVALID TASK TEST MAIN ==========')
    try:
        await main()
        print("WORK FINE!")
    except Exception as e:
        print("CRASH!")

async def test_all():
    test_get_task_id_from_task_result_file_path_delete_invalid_task()
    test_get_to_be_deleted_file_path_delete_invalid_task()
    test_main_delete_invalid_task()


