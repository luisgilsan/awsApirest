from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from django.db.models import Sum,Count
from django.db.models import Q
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey

from .models import (Folder,
    FolderCategory,
    File,
    FileType,
    FilesRegister,
    )
from .serializers import (FolderSerializer,
    FolderCategorySerializer,
    FileSerializer,
    FileTypeSerializer,
    FilesRegisterSerializer
    )

# Create your views here.
class FolderViewSet(viewsets.ModelViewSet):
    """ Define el queryset para la ApiRest del modelo: Folder """

    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def create(self, *args, **kwargs):
        print("se creo un folder")
        print("se creo un folder")
        return super(FolderViewSet, self).create(*args, **kwargs)

class FolderCategoryViewSet(viewsets.ModelViewSet):
    """ Define el queryset para la ApiRest del modelo: FolderCategory """
    queryset = FolderCategory.objects.all()
    serializer_class = FolderCategorySerializer

class FileViewSet(viewsets.ModelViewSet):
    """ Define el queryset para la ApiRest del modelo: File """
    queryset = File.objects.all()
    serializer_class = FileSerializer

class FileTypeViewSet(viewsets.ModelViewSet):
    """ Define el queryset para la ApiRest del modelo: FileType """
    queryset = FileType.objects.all()
    serializer_class = FileTypeSerializer

class FilesRegisterViewSet(viewsets.ModelViewSet):
    """ Define el queryset para la ApiRest del modelo: FileType """
    queryset = FilesRegister.objects.all()
    serializer_class = FilesRegisterSerializer


class DeleteFolderView(APIView):
    """ Controla eliminacion del modelo Folder """

    def delete(self,request,*args,**kwargs):
        """
            Se realiza control del borrado de carpeta con contenido. 
        """
        folder=Folder.objects.filter(id=self.kwargs['id'],files__isnull=True,childs__isnull=True)
        if folder:
            folder.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            queryset=File.objects.filter(folder=self.kwargs['id']).values()
            return Response(queryset,status=status.HTTP_409_CONFLICT)

class CountFolderSizeView(APIView):
    """ Define ApiRest para colsulta peso del folder. """

    def get(self,request,*args,**kwargs):
        """
            Retorna el tamaño total de archivos contenidos 
            dentro de la carpeta.
        """
        folder = Folder.objects.filter(id=self.kwargs['id']).first()
        status_response = status.HTTP_200_OK
        if folder:
            json_response = {'total_size_folder':folder.compute_total_size_subfolders()}
        else:
            json_response = {'404 Folder not found!'}
            status_response = status.HTTP_404_NOT_FOUND        
        return Response(json_response,status=status_response)

class CountFileView(APIView):
    """ Define ApiRest para colsulta de archivos contenidos en el folder. """

    def get(self,request,*args,**kwargs):
        """
            Retorna el numero de achivos de una carpeta
            agrupados por tipo de archivo.
        """
        folder = Folder.objects.filter(id=self.kwargs['id']).first()
        status_response = status.HTTP_200_OK
        if folder:
            json_response = folder.return_num_files_by_type()
        else:
            json_response = {'404 Folder not found!'}
            status_response = status.HTTP_404_NOT_FOUND         
        return Response(json_response,status=status_response)

class FilesEstructureView(APIView):
    """ Define ApiRest que retorna estructura de los folders. """

    def get(self,request,*args,**kwargs):
        """
            Retorna la estructura de los folders en formato JSON.
        """
        folders=Folder.objects.filter(parent__isnull=True)
        dict_folders = {}
        for folder in folders:
            dict_folders.update({folder.name:folder.compute_estructure_subfolders()})
        return Response(dict_folders,status=status.HTTP_200_OK)