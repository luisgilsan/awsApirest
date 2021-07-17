from django.urls import path
from folders import views

urlpatterns = [
    path('folders_delete/<int:id>', views.DeleteFolder.as_view(), name='Delete Folder'),
    path('CountSize/<int:id>', views.CountSize.as_view(), name='Count Size'),
    path('CountFile/<int:id>', views.CountFile.as_view(), name='Count File'),
    path('SubfilesFiles/', views.SubfilesFiles.as_view(), name='Subfile File'),
]