from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from collections import OrderedDict

import os
import model

r_model = model.R()

@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    global r_model
    r_model = model.R()

    context = {'scriptNames': init_script_list(),}

    return render(request, 'r_app/home.html', context)



@login_required()
def scriptView(request):
    """
    Controller for the script view page.
    """

    context = {}

    if request.GET and 'filename' in request.GET:
        filename = request.GET['filename']

        r_model.filename = filename

        read_code()
        context = {'code': r_model.code, 'filename': filename}

    return render(request, 'r_app/scriptView.html', context)



@login_required()
def scriptRun(request):
    """
    Controller for the script view page.
    """

    context = {}

    if request.GET and 'filename' in request.GET:
        filename = request.GET['filename']

        # if file has not been initialized into model yet - if accessed run page before going to view page
        if r_model.filename == "" or r_model.filename != filename:
            r_model.filename = filename
            read_code()

        params = parse_code()

        context = {'filename': filename,
                   'host': request.get_host(),
                   'params': params}

    return render(request, 'r_app/scriptRun.html', context)


def init_script_list():

    scripts = []

    for root, dirs, files in os.walk("/var/FastRWeb/web.R/tethys-scripts"):
        for file in files:
            if file.endswith('.R') or file.endswith('.r'):
                scripts.insert(scripts.__len__(), file)

    return scripts


def read_code():

    if r_model.filename != "":
        with open("/var/FastRWeb/web.R/tethys-scripts/" + r_model.filename, 'r') as script:
            r_code = script.read()
            r_model.code = r_code


def parse_code():
    # parse code for parameter names
    start_code = "run <- function("
    index = r_model.code.find(start_code) + start_code.__len__()

    declaration = r_model.code[index:r_model.code.find(')')]
    split_code = [x.strip() for x in declaration.split(',')]

    params = OrderedDict()

    for string in split_code:

        attributes = {}
        param = ""
        value = ""  # default value
        readingValue = False

        for char in string:

            if char == "," or char == ".":
                readingValue = False
                break
            elif char == "=":
                readingValue = True
            elif readingValue:
                value += char
            else:
                param += char

        if param != "":
            attributes['value'] = value.strip()

            params[param.strip()] = attributes

    for key in params:
        start_code = "#" + key
        index = r_model.code.find(start_code)

        doc = r_model.code[index:r_model.code.find('\n', index)]

        try:
            split_doc = doc.split(',')
            param_name = split_doc[1] + '(' + key + ')'

            # set attribute name
            params[key]['name'] = param_name
            params[key]['type'] = split_doc[2]

        except IndexError:  # if documentation for this parameter does not exist
            params[key]['name'] = key
            params[key]['type'] = "string"

    print params

    return params
