
import time
from datetime import datetime
from html2text import HTML2Text
from django.template import Library, Node, TemplateSyntaxError
register = Library()

# custom template filter - place this in your custom template tags file


@register.filter
def since_when(value):
    """
    Filter - removes the minutes, seconds, and milliseconds from a datetime

    Example usage in template:

    {{ my_datetime|only_hours|timesince }}

    This would show the hours in my_datetime without showing the minutes or seconds.
    """
    if not value: return value

    # secondsSince = datetime.now().timestamp() - value.timestamp() # datetime.timestamp(value)
    secondsSince = datetime.now().timestamp() - time.mktime(datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S.%f%z").timetuple())


    units = (
        ('second', 1, ('ثانية', 'ثانيتين', 'ثواني')),
        ('minute', 60, ('دقيقة', 'دقيقتين', 'دقائق')),
        ('hour', 60 * 60, ('ساعة', 'ساعتين', 'ساعات')),
        ('day', 60 * 60 * 24, ('يوم', 'يومين', 'أيام')),
        ('week', 60 * 60 * 24 * 7, ('أسبوع', 'أسبوعين', 'أسابيع')),
        ('month', 60 * 60 * 24 * 30, ('شهر', 'شهرين', 'شهور')),
        ('year', 60 * 60 * 24 * 30 * 12, ('سنة', 'سنتين', 'سنين')),
    )

    phrase = 'منذ {0}'
    for unit, period, arabic in units[::-1]:
        since = int(secondsSince / period)
        if since > 0:
            '''
            since = 1 => [0]
            since = 2 => [1]
            since > 2 => [2]
            since > 10 => [0]
            '''
            if since == 1:
                since = arabic[0]
            elif since == 2:
                since = arabic[1]
            elif 2 < since <= 10:
                since = f'{since} {arabic[2]}'
            else:
                since = f'{since} {arabic[0]}'

            return phrase.format(since)
    return phrase.format('ثانية')



@register.filter
def trim(value):
    return value.strip()


@register.filter
def html2text(value):
    h = HTML2Text()

    h.ignore_links = True
    h.ignore_emphasis = True
    h.ignore_images = True
    h.ignore_tables = True

    return h.handle(value).strip()

@register.filter
def operator_or(value, new):
    return value or new

from django import template
from django.template.defaulttags import URLNode, url

register = template.Library()

class AbsURLNode(URLNode):
    def __init__(self, view_name, args, kwargs, asvar):
        super().__init__(view_name, args, kwargs, asvar)

    def render(self, context):
        url     = super().render(context)
        request = context['request']

        return request.build_absolute_uri(url)


@register.tag
def abs_url(parser, token):
    # use: {% abs_url 'view_name' post.pk %}
    urlNode = url(parser, token)
    return AbsURLNode( urlNode.view_name, urlNode.args, urlNode.kwargs, urlNode.asvar  )

@register.filter
def sumition(value, arg):
    result =  int(value) + int(arg)
    return result

@register.filter
def subtract(value, arg):
    result =  int(value) - int(arg)
    return result