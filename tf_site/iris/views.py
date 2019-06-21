import os 

from django import forms 
from django.contrib import messages
from django.db.models import Count 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import generic

from .forms import IrisEditForm, NameForm, UploadFileForm #, ModelFormWithFileField
from .models import Iris

class IndexView(generic.ListView): 
    template_name = 'iris/index.html'
    context_object_name = 'iris_list'

    def get_queryset(self): 
        context = {
            'count': Iris.objects.all().count(),
            'classifications': Iris.objects.values('classification').annotate(Count('classification')),
            'one': 1, 
            'two': 2,
        }
        return context

class DetailView(generic.DetailView): 
    model = Iris 
    template_name = 'iris/detail.html'

    def get_queryset(self): 
        return Iris.objects.all().filter() #.filter(id=pk)
        # context = {
        #     'Iriss': Iris.objects.all().first()
        # }
        # return context 
 
class UpdateView(generic.UpdateView):
    model = Iris 
    fields = {'petal_width', 'petal_length', }
    template_name = 'iris/update.html',
    # pk_url_kwarg = 'iris_pk',
    # context_object_name = 'post'
    # form_class = IrisEditForm

    # def get_queryset(self):
        # return Iris.objects.all().filter() 

class IrisUpdate(generic.UpdateView):
    model = Iris 
    fields = ['id', 'sepal_width', 'sepal_length', 'petal_width', 'petal_length', 'classification']
    template_name_suffix = '_update_form'


class CreateView(generic.CreateView):
    model = Iris 
    fields = ['sepal_width', 'sepal_length', 'petal_width', 'petal_length', 'classification']
    success_url = '/iris/upload/success/'


def create(request):
    return HttpResponse("<h1>Create</h1>")



def index(request):
    return HttpResponse("<h1>Index Page</h1>")


# class FileUploadView(generic.FormView):
#     # model = Iris 
#     template_name = 'iris/upload.html'


def load_model(data, mode):
    """ 
    Handles different ways data can be loaded to a model
    append: adds new data to existing data
        - primary key: auto increment id
    replace: clears all data from the model, then loads data
    """
    print('mode: ', mode)
    print('data&&: ', data)

    if mode == 'append':
        model_load(data)

    elif mode == 'replace':
        model_clear()
        model_load(data)

    
def model_load(data):
    """ 
    Loads data to a model
    """
    for line in data:
        sl, sw, pl, pw, c = line.split(',')
        c = c.strip() # all but last record has invisible newline character that should be removed
        i = Iris(petal_length=pl, petal_width=pw, sepal_length=sl, sepal_width=sw, classification=c) 
        i.save()


def model_clear():
    """
    Wipes data from a model
    """
    Iris.objects.all().delete()

    # Raw SQL is needed to update the system table that tracks the row number/pk id
    # without resetting to 0 on a clear, the numbering will continue after objects are deleted
    from django.db import connection 
    with connection.cursor() as cursor: 
        cursor.execute("UPDATE sqlite_sequence SET SEQ = 0 WHERE NAME = 'iris_iris'")




def handle_uploaded_file(file, name, load=False, mode=None):
    """ 
    Move this to another file for handling files/requests/forms
    file: data
    name: filename in directory
    load: data is written to model
    mode: None if load=F, Append, Replace
    """

    print('load**: ', load)
    print('mode**: ', mode)



    # current working directory of file
    save_dir = os.path.dirname(os.path.realpath(__file__))
    # append location for dataset storage
    save_dir = os.path.join(save_dir, 'static/tf_site/datasets/')

    # apply timestamp to filename for unique name?
    # this use case may want to overwrite files and not retain historical versions

    with open(os.path.join(save_dir, name), 'wb+') as destination:
        # print('destination: ', destination)
        # print('file: ', file)
        # print('name: ', name)

        for chunk in file.chunks():
            destination.write(chunk)

    print('loading...', file, mode)
    with open(os.path.join(save_dir, name), 'r') as dest:
        print('opened dest')
        next(dest) # skip over header
        if load:
            # for line in dest: 
            load_model(dest, mode)
                # print ('lline: ', line) 
            
                


def FileUploadView(request):
    # from io import TextIOWrapper

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # wrap the file to preserve encoding
        # print('FILES: ', request.FILES['file'])
        # wrapped_file = TextIOWrapper(request.FILES['file'], encoding=request.encoding)

        # create a form instance and populate it with data from the request:
        form = UploadFileForm(request.POST, request.FILES, initial={'action': 'append'})
        # form = UploadFileForm(request.POST, wrapped_file, initial={'action': 'append'})

        # form.fields['action'].initial = 'append'

        # check whether it's valid:
        if form.is_valid():
            # form['title'].data is the value from the form's title field (what the filename should be saved as)
            handle_uploaded_file(request.FILES['file'], form['title'].data, form['load'].data, form['action'].data)

            # Redirect with success message
            msg = form['title'].data 
            msg += ' was successfully uploaded.'
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect('/iris/browse')
    else:
        # if a GET (or any other method) we'll create a blank form
        form = UploadFileForm()
    return render(request, 'iris/upload.html', {'form': form})


def upload_success(request):
    return HttpResponse('<h1>File was successfully uploaded</h1>')


def get_file_contents(request, file_name=None, req=False): 
    """
    Returns the first row of a file, which is intended to be column headings.
    file_name: the name of the file in the static/tf_site/datasets/ folder being read
    req: this is called from another function (True) or ajax (False/default)
    """
    import csv 

    # file_name in ajax request
    if file_name == None:
        file_name = request.GET.get('filename')

    # filepath to files
    dir = os.path.dirname(os.path.realpath(__file__))
    dir = os.path.join(dir, 'static/tf_site/datasets/')

    # open the file and get the first line (header names)
    with open(os.path.join(dir, file_name)) as f:
        reader = csv.reader(f)
        first_row = next(reader)    

    # if called from other function, return list
    if req:
        return first_row
    else: 
        # if called from ajax, return json response object
        return JsonResponse({'first_row': first_row})


def browse_file(request, file_name='iris.csv'):
    """
    Loads the csv file and reads the header record for column names
    TODO: add summary statistics for each column in file
    -   allow specific attributes to be set (categorical/ordinal/target/etc)
    """

    # filepath to files
    save_dir = os.path.dirname(os.path.realpath(__file__))
    save_dir = os.path.join(save_dir, 'static/tf_site/datasets/')

    first_row = get_file_contents(request, file_name, req=True)

    # get the contents of the directory to display on the page
    from os import listdir
    from os.path import isfile, join
    allfiles = [f for f in listdir(save_dir) if isfile(join(save_dir, f))]
    
    # process file list and select files ending in .csv
    onlyfiles = []
    for f in allfiles:
        ext = f[-4:]
        if ext == '.csv':
            onlyfiles.append(f)

    print('filename: ', file_name)

    return render(request, 'iris/browse.html', {'header': first_row, 'files': onlyfiles})






# def upload_file(request):
#     if request.method == 'POST':
#         form = ModelFormWithFileField(request.POST, request.FILES)
#         if form.is_valid():
#             # file is saved
#             form.save()
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = ModelFormWithFileField()
#     return render(request, 'upload.html', {'form': form})

# def FileUpload2View(request):
#     return HttpResponse('<h1>Upload2</h1>')


# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#         # return HttpResponse("<h1>get_name else entered</h1>")


#     return render(request, 'iris/name.html', {'form': form})



