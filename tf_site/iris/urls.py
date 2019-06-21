from django.contrib import admin
from django.urls import path

from . import views

app_name = 'iris'
urlpatterns = [
    # /iris/
    path('', views.IndexView.as_view(), name='index'),

    # /iris/432
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    # /iris/432/edit
    path('<int:pk>/edit/', views.UpdateView.as_view(), name='edit'),

    # /iris/upload 
    path('upload/', views.FileUploadView, name='upload'),

    # /iris/upload/success
    path('upload/success/', views.upload_success, name='upload-success'),

    # /iris/browse
    path('browse/', views.browse_file, name='browse'),

    # /iris/browse/ajax
    path('browse/ajax/file/', views.get_file_contents, name='get-file'),

    # /iris/create
    # path('create/', views.create, name='create'),
    path('create/', views.CreateView.as_view(), name='create'),

    # /iris/432/update
    path('<int:pk>/update/', views.IrisUpdate.as_view(), name='update'),



   # ex: /iris/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),

    # ex: /iris/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]



