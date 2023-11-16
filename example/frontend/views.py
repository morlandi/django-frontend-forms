import os
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.utils.html import escape
from django.template.loader import render_to_string


sections = [
    {
        'title': '',
        'pages': [
            {'index': 1, 'title': 'Introduction', },
        ]
    },
    {
        'title': 'Basic modals',
        'pages': [
            {'index': 2, 'title': 'HTML popup windows do not exist', },
            {'index': 3, 'title': 'A basic modal box with pure Javascript', },
            {'index': 4, 'title': 'A modal which returns a value', },
            {'index': 5, 'title': 'Bootstrap modal plugin', },
        ]
    },
    {
        'title': 'Basic modals in a Django template',
        'pages': [
            {'index': 6, 'title': 'Objectives', },
            {'index': 7, 'title': 'Usage', },
            {'index': 8, 'title': 'Opening a Dialog', },
            {'index': 9, 'title': 'Dialog methods and options', },
            {'index': 10, 'title': 'Dialog notifications', },
            {'index': 11, 'title': 'Examples', },
            {'index': 12, 'title': 'Files organization', },
        ]
    },
    {
        'title': 'Form submission from a modal',
        'pages': [
        ]
    },
    {
        'title': 'Creating or updating a Django Model in the front-end',
        'pages': [
        ]
    },
    {
        'title': 'Creating or updating a Django Model (revised)',
        'pages': [
        ]
    },
    {
        'title': 'Advanced forms',
        'pages': [
        ]
    },
]


def get_last_page_index():
    for i in range(len(sections)-1, -1, -1):
        section = sections[i]
        if section['pages']:
            page_index = section['pages'][-1]['index']
            return page_index
    return 0

def get_page_template_name(page):
    return "pages0/%d.html" % page

def get_page_template_path(page):
    return os.path.abspath(os.path.join('.', 'frontend', 'templates', 'pages0', '%d.html' % page
))


def page(request, page):

    def get_page_title(page_index):
        for section in sections:
            for page in section['pages']:
                if page['index'] == page_index:
                    return page['title']
        return ''

    template_name = "pages0/%d.html" % page

    return render(request, get_page_template_name(page), {
        'page_index': page,
        'page_title': get_page_title(page),
        'sections': sections,
        'previous_page': reverse('frontend:page', args=(page-1, )) if page > 1 else None,
        'next_page': reverse('frontend:page', args=(page+1, )) if page < get_last_page_index() else None,
    })


def code(request, page):
    filename = get_page_template_path(page)
    with open(filename, "r") as f:
        text = f.read()
    html = '<pre>' + escape(text) + '</pre>'
    return HttpResponse(html)

