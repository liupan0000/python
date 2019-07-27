from time import sleep

from celery import Celery
from celery.schedules import crontab


app = Celery("tasks",broker="redis://localhost:6379/1")

@app.task

def send_mail():
#
# def send_mail(sender,**kargs):
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         # test.s('Happy Mondays!'),
#     )
    sleep(5)

    return "发送成功"

if __name__=="__main__":
    result = send_mail.delay()
    print(result)