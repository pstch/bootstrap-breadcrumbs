# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2012 by Å�ukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django import template


register = template.Library()


CONTEXT_KEY = 'DJANGO_BREADCRUMB_LINKS'


def breadcrumb(context, label, viewname=None, *args):
    """
    Add link to list of breadcrumbs, usage:

    {% load bubbles_breadcrumbs %}
    {% breadcrumb "Home" "index" %}

    Remember to use it inside {% block %} with {{ block.super }} to get all
    parent breadcrumbs.

    :param label: Breadcrumb link label
    :param viewname: Name of the view to link this breadcrumb to.
    :param args: Any arguments to view function.
    """
    context['request'].META[CONTEXT_KEY] = context['request'].META.get(
        CONTEXT_KEY, []) + [(label, viewname, args)]
    return ''


def render_breadcrumbs(context):
    """
    Render breadcrumbs html using twitter bootstrap css classes.
    """
    links = []
    for (label, viewname, args) in context['request'].META.get(CONTEXT_KEY, []):
        if viewname:
            try:
                url = reverse(viewname=viewname, args=args)
            except NoReverseMatch:
                url = viewname
        else:
            url = None
        links.append((url, _(label) if label else label))

    if not links:
        return ''

    ret = '<ul class="breadcrumb">'
    total = len(links)
    i = 1
    for (url, label) in links:
        ret += '<li>'
        if total > 1 and i < total:
            if url:
                ret += '<a href="%s">%s</a>' % (url, label)
            else:
                ret += '<a>%s</a>' % (label)
            ret += ' <span class="divider">/</span>'
        else:
            ret += '<a>%s</a>' % (label)
        ret += '</li>'
        i += 1
    ret += '</ul>'
    return mark_safe(ret)


register.simple_tag(takes_context=True)(breadcrumb)
register.simple_tag(takes_context=True)(render_breadcrumbs)
