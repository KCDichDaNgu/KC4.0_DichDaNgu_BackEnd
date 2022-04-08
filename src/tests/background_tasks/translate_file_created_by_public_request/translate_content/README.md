# Module kiểm thử nhóm 7
Mục đích:kiểm thử các function ,đảm bảo dịch các tệp được tạo theo public request
Trong backend/src/infrastructure/configs/main.py thêm cấu hình cho các background tasks mới
        

"test_translate_file_created_by_public_request.translate_content.docx": BackgroundTask(
ID="test_translate_file_created_by_public_request.translate_content.docx",
TRIGGER=BackgroundTaskTriggerEnum.interval.value,
CONFIG=dict(seconds=0, max_instances=1),
   ),


"test_translate_file_created_by_public_request.translate_content.pptx": BackgroundTask(
ID="test_translate_file_created_by_public_request.translate_content.pptx",
TRIGGER=BackgroundTaskTriggerEnum.interval.value,
CONFIG=dict(seconds=0, max_instances=1),
),

+Trong /backend/src/tests/background_tasks/main.py thêm

from tests.background_tasks.translate_file_created_by_public_request.translate_content.docx import add_fresh_jobs as add_fresh_jobs_3
from tests.background_tasks.translate_file_created_by_public_request.translate_content.pptx import add_fresh_jobs as add_fresh_jobs_4

Và:

new_background_task_scheduler = add_fresh_jobs_3(new_background_task_scheduler, BACKGROUND_TASKS)
new_background_task_scheduler = add_fresh_jobs_4(new_background_task_scheduler, BACKGROUND_TASKS)

+Trong background_tasks/translate_file_created_by_public_request/translate_content/docx
và     background_tasks/translate_file_created_by_public_request/translate_content/pptx chứa phần test

