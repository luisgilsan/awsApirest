from django.urls import path
from folders import views

urlpatterns = [
    path('folders_delete/<int:id>', views.CountFolderSizeView.as_view(), name='delete_folder'),
    path('countsize/<int:id>', views.CountFolderSizeView.as_view(), name='count_size'),
    path('countfiles/<int:id>', views.CountFileView.as_view(), name='countfiles'),
    path('filesestructure/', views.FilesEstructureView.as_view(), name='filesestructure'),
]