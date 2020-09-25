from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse

from .models import Signup


def signup_newsletter(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    email = request.POST.get('email', None)
    if not email:
        return HttpResponseBadRequest()

    elm = Signup(email=email)
    elm.save()

    return HttpResponse(status=200)
