from django.shortcuts import render
from django.views.defaults import server_error
from django.http import HttpResponseBadRequest
import codecs
from config.bad_words import BAD_WORDS

START_INDEX = 9
INDEX_HTML = 'index.html'
SERVER_ERROR_HTML = 'server-error.html'

def filter_bad_words(file):
    result = ''
    for line in file:
        line = codecs.decode(line, 'ISO-8859-1')
        if not any(bad_word in line for bad_word in BAD_WORDS):
            try:
                if line[START_INDEX] == ']':
                    result += line[START_INDEX + 1:].lstrip()
                else:
                    result += line[START_INDEX:].lstrip()
            except IndexError:
                continue
    return result

def index(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('document')
        if not uploaded_file:
            return render(request, INDEX_HTML, {'show_warning': True})
        filtered_result = filter_bad_words(uploaded_file)
        return render(request, INDEX_HTML, {'result': filtered_result})
    return render(request, INDEX_HTML)

def handler500(request, *args, **argv):
    return server_error(request, template_name=SERVER_ERROR_HTML)
