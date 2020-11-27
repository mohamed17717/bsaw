from django.views.decorators.http import require_http_methods
from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseForbidden,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)

import json
from datetime import datetime


# may cause error in get params byt i hope not
def extract_request_data(func):
    def wrapper(request, *args, **kwargs):
        method = request.POST if request.method == 'POST' else request.GET
        data = method.dict()
        if not bool(data):
            data = json.loads(request.body.decode('utf8'))
        return func(request, data, *args, **kwargs)
    return wrapper


def is_from_myApp(func):
    @extract_request_data
    def wrapper(request, data, *args, **kwargs):
        appKey = data.get('itsme', '')

        todayDate = datetime.now()
        def sumNumDigits(num): return sum([int(i) for i in str(num)])
        dynamicLength = int(
            f'{sumNumDigits(todayDate.year)}{sumNumDigits(todayDate.month)}{sumNumDigits(todayDate.day)}')

        if dynamicLength != len(appKey):
            return HttpResponseForbidden()

        return func(request, *args, **kwargs)
    return wrapper


def extract_post_request_data(func):
    def wrapper(request, *args, **kwargs):

        data = request.POST.dict()
        if not bool(data):
            data = json.loads(request.body.decode('utf8'))

        return func(request, data, *args, **kwargs)
    return wrapper


def check_unique_fields(kls, uniqueFields=[]):
    def decorator(func):
        @extract_post_request_data
        def wrapper(request, data, *args, **kwargs):

            for field in uniqueFields:
                value = data.get(field)
                if kls.objects.filter(**{field: value}).first():
                    return HttpResponseBadRequest(f'{field}: "{value}" is already in use')

            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_fields(requiredFields=[]):
    def decorator(func):
        @extract_post_request_data
        def wrapper(request, data, *args, **kwargs):

            for field in requiredFields:
                if not data.get(field, None):
                    return HttpResponseBadRequest(f'field "{field}" is required')

            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def allow_fields(allowed_fields=[]):
    def decorator(func):
        @extract_post_request_data
        def wrapper(request, data, *args, **kwargs):
            for field in data.keys():
                if field not in allowed_fields:
                    return HttpResponseBadRequest(f'field "{field}" is not allowed')

            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def validateToken():
    pass


# field alias
# content => article => articleHTML
