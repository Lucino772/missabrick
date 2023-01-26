from missabrick import celery
from celery.schedules import crontab
# from scripts.load_rebrickable import run

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwds):
    print('Setup periodic tasks')
    sender.add_periodic_task(
        crontab(minute='0', hour='*/12', day_of_month='*', month_of_year='*'),
        load_rebrickable.s()
    )

@celery.task
def load_rebrickable():
    print('Hello World !')
