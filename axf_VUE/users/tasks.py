from time import sleep

from celery import shared_task
from django.core.mail import send_mail

from axf_VUE.settings import EMAIL_HOST_USER


@shared_task

def send_code():

    print("准备发送")

    sleep(5)
    print("发送完毕")


@shared_task

def send_email_asy(u_email,subject,html_msg):
    send_mail(subject=subject, message="", from_email=EMAIL_HOST_USER, recipient_list=(u_email,),
              html_message=html_msg)


@shared_task
def send_msg(x,y):
    return x+y



