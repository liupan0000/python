from django.contrib import messages
from django.shortcuts import render
from rest_framework.status import HTTP_200_OK


def index(request):

    # data = {
    #
    #     "info":request.session.get("info")
    # }
    #
    # request.session.flush()

    data = {
        "messages":messages.get_messages(request)
    }

    return render(request,"index.html",context=data)