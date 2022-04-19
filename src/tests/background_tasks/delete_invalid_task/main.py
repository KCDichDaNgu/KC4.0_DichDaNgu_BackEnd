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
    print("Test_get_to_be_deleted_file_path test case 0: ", get_to_be_deleted_file_path([]) == ([], [], []))
    print("Test_get_to_be_deleted_file_path test case 1: ",get_to_be_deleted_file_path(["filepath1.txt"]) == (["task_result/filepath1.txt"], ["file_translation/filepath1/", "file_language_detection/filepath1/"]))
    print("Test_get_to_be_deleted_file_path test case 2: ", get_to_be_deleted_file_path(["/doc/file.txt", "/usr/bin/go"]) == (["task_result/file.txt", "task_result/usr/bin/go/"], ["file_translation/doc/file/", "file_translation/usr/bin/go/"], ["file_language_detection/doc/file/", "file_language_detection/usr/bin/go/"]))
    print("Test_get_to_be_deleted_file_path test case 3: ", get_to_be_deleted_file_path(["a"]) == (["task_result/a"], ["file_translation/a/"], ["file_language_detection/a/"]))
    print("Test_get_to_be_deleted_file_path test case 4: ", get_to_be_deleted_file_path(["/usr/bin/go__what.txt"]) == (["task_result/usr/bin/go__what.txt"], ["file_translation/what/"], ["file_language_detection/what/"]))
    

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


