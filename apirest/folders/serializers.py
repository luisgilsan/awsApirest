from django.contrib.auth.models import User, Group
from rest_framework import serializers, viewsets
from .models import (Folder,
    FolderCategory,
    File,
    FileType,
    FilesRegister
    )

class FolderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Folder
        fields = ['id','name', 'category', 'parent']

class FolderCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FolderCategory
        fields = ['id','name', 'icon',]

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['id','name','folder','path','file_type_id','lines','size_in_kb']

class FileTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileType
        fields = ['id','name', 'icon']

class FilesRegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FilesRegister
        fields = ['id',
            'name', 
            'csv_lines',
            'csv_size_in_kb',
            'txt_lines',
            'txt_size_in_kb',
        ]
