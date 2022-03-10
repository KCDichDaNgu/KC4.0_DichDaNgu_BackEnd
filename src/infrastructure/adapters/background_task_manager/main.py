from core.ports.background_task_manager import BackgroundTaskManagerPort
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class BackgroundTaskManager(BackgroundTaskManagerPort):

    scheduler: AsyncIOScheduler = None

    def __init__(self, scheduler: AsyncIOScheduler = None, force_assignment: bool = False) -> None:
        
        if self.__class__.scheduler is None or force_assignment == True:
            self.__class__.scheduler = scheduler

    def start(self):
        self.__class__.scheduler.start()

    def stop(self):

        self.__class__.scheduler.shutdown()

    def add_job(self, func, **kwargs):
        
        self.__class__.scheduler.add_job(func, **kwargs)

    def get_job(self, job_id, **kwargs):

        return self.__class__.scheduler.get_job(job_id, **kwargs)

    def get_jobs(self, **kwargs):
        
        return self.__class__.scheduler.get_jobs(**kwargs)

    def remove_all_jobs(self, **kwargs):

        return self.__class__.scheduler.remove_all_jobs(**kwargs)
    
    def remove_job(self, job_id, jobstore=None):
        return self.__class__.scheduler.remove_job(job_id, jobstore)

