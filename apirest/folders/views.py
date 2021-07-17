from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from django.db.models import Sum,Count
from django.db.models import Q

from .models import (Folder,
    FolderCategory,
    File,
    FileType,
    )
from .serializers import (FolderSerializer,
    FolderCategorySerializer,
    FileSerializer,
    FileTypeSerializer
    )

# Create your views here.
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

class FolderCategoryViewSet(viewsets.ModelViewSet):
    queryset = FolderCategory.objects.all()
    serializer_class = FolderCategorySerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

class FileTypeViewSet(viewsets.ModelViewSet):
    queryset = FileType.objects.all()
    serializer_class = FileTypeSerializer


class DeleteFolder(APIView):
    def delete(self,request,*args,**kwargs):
        folder=Folder.objects.filter(id=self.kwargs['id'],files__isnull=True)
        if folder:
            folder.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            queryset=File.objects.filter(folder=self.kwargs['id']).values()
            return Response(queryset,status=status.HTTP_409_CONFLICT)

class CountSize(APIView):
    def get(self,request,*args,**kwargs):
        anwr=File.objects.filter(folder=self.kwargs['id']).aggregate(Sum('size_in_kb'),Count('id'))
        return Response(anwr,status=status.HTTP_200_OK)

class CountFile(APIView):
    def get(self,request,*args,**kwargs):
        f=Folder.objects.filter(Q(id=self.kwargs['id'])|Q(parent=self.kwargs['id'])).values_list('id',flat=True)
        anwr=File.objects.filter(folder__in=f).values('file_type_id').annotate(count=Count('file_type_id'))
        return Response(anwr,status=status.HTTP_200_OK)

class SubfilesFiles(APIView):
    def get(self,request,*args,**kwargs):
        folder=Folder.objects.filter(parent__isnull=True)
        folder2=Folder.objects.filter(parent__isnull=True)
        print(folder)
        return Response(status=status.HTTP_200_OK)