from django.db import models
import os
from django.conf import settings
from pathlib import Path
import os 
from django.http import JsonResponse
import threading
import time
from django.db.models import Q

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# Create your models here.

class FolderCategory(models.Model):
    """ Define los atributos del modelo: Categoria del folder. """
    
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='category_icons')

    def __str__(self):
        """ 
            Nombre del registro en el ORM
        """
        return self.name

    class Meta:
        """ 
            Nombre del modelo en el panel Admin
        """
        verbose_name = 'Folder Category'
        verbose_name_plural = 'Folder Categories'

class FilesRegister(models.Model):
    """ 
        Define los atributos del modelo: FilesRegister. 

        En este modelo se registra el acumulado de los archivos almacenados.
        La creacion se ejecuta desde el hilo de los archivos
    """
    
    name = models.DateTimeField(auto_now_add=True)
    csv_lines = models.IntegerField(verbose_name="Lines",default=0)
    csv_size_in_kb = models.FloatField(verbose_name="Size (KB)",default=0)
    txt_lines = models.IntegerField(verbose_name="Lines",default=0)
    txt_size_in_kb = models.FloatField(verbose_name="Size (KB)",default=0)

class File(models.Model):
    """ Define los atributos del modelo: Archivo. """
    
    name = models.CharField(max_length=100, unique=True)
    folder = models.ForeignKey("Folder", related_name='files',
        verbose_name="Folder", on_delete=models.CASCADE)
    path = models.CharField(max_length=255, verbose_name="Path")
    file_type_id = models.ForeignKey("FileType", related_name='files',
        blank=True,null=True, verbose_name="File Type", on_delete=models.SET_NULL)
    lines = models.IntegerField(verbose_name="Lines",default=0)
    size_in_kb = models.FloatField(verbose_name="Size (KB)",default=0)

    def __str__(self):
        """ Nombre del registro en el ORM
        """
        return self.name

    class Meta:
        """ Nombre del modelo en el panel Admin
        """
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def thread_store_total_size_and_lines(self,name):
        """ 
            Subproceso para calculo y almacenamiento de 
            recuento de archivos.
        """
        print("Thread %s: starting" % (name,))
        time.sleep(2)
        files = File.objects.filter(Q(file_type_id__name__icontains='CSV') |
                Q(file_type_id__name__icontains='TXT'))
        csv_total_kb = 0
        csv_total_lines = 0
        for line in filter(lambda file: file.file_type_id.name == 'CSV', files ):
            csv_total_kb += line.size_in_kb 
            csv_total_lines += line.lines
        txt_total_kb = 0
        txt_total_lines = 0
        for line in filter(lambda file: file.file_type_id.name == 'TXT', files ):
            txt_total_kb += line.size_in_kb 
            txt_total_lines += line.lines
        FilesRegister.objects.create(
            csv_size_in_kb=csv_total_kb,
            csv_lines=csv_total_lines,
            txt_size_in_kb=txt_total_kb,
            txt_lines=txt_total_lines,
        )
        print("Thread %s: finishing" % (name,))

    def save(self, *args, **kwargs):
        """ 
            Extiende el guardado del registro para añadir 
            subproceso.
        """
        thread = threading.Thread(target=self.thread_store_total_size_and_lines, args=("hilo 1",))
        thread.start()
        super(File, self).save(*args, **kwargs)

class FileType(models.Model):
    """ Define los atributos del modelo: Tipo de archivo. """
    
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='type_icons')

    def __str__(self):
        """ Nombre del registro en el ORM
        """
        return self.name

    class Meta:
        """ Nombre del modelo en el panel Admin
        """
        verbose_name = 'Type'
        verbose_name_plural = 'Types'

class Folder(models.Model):
    """ Define los metodos y atributos del modelo: Carpeta. """
    
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey("FolderCategory", related_name='files',
        blank=True,null=True, verbose_name="Categoria", on_delete=models.SET_NULL)
    parent = models.ForeignKey("Folder", related_name='childs',
        blank=True,null=True, verbose_name="Folder padre", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'

    def delete(self):
        """Restriccion carpeta con datos.

        Se extiende la funcion de borrador para 
        evitar la eliminacion de un folder con
        archivos o subcarpetas
        
        """
        if self.files.all() or self.childs.all():
            return None
        super(Folder, self).delete()

    def compute_files_size(self):
        """Retorna tamaño de archivos.

        Itera archivos contenidos en la carpeta y
        suma peso en kb.
        
        """
        total_size = 0
        for file in self.files.all():
            total_size += file.size_in_kb
        return total_size

    def compute_files_size_by_type(self,filetype):
        """Retorna numero de archivos contenidos
        en la carpeta.

        Itera archivos contenidos la carpeta 
        para sumar el numero de archivos.
        
        """
        total_files = 0
        files = filter(lambda file: file.file_type_id == filetype, self.files.all())
        for file in files:
            total_files += 1
        return total_files
            
    def return_num_files_by_type(self):
        """Retorna cantidad de archivos
        agrupados por tipo de archivo.

        Itera archivos contenidos en la carpeta y
        suma en un diccionario los archivos por 
        su tipo.
        
        """
        filetypes = FileType.objects.all()
        dict_types = {}
        for filetype in filetypes:
            qty = self.compute_num_files_by_type(filetype)
            dict_types.update({filetype.name:qty})
        return dict_types

    def compute_num_files_by_type(self,filetype):
        """Retorna numero de archivos agrupados 
        por tipo de archivo contenidos en las subcarpetas.

        Itera archivos contenidos las subcarpetas 
        para sumar el numero de archivos almacenados
        
        """
        childs_num= 0
        childs_num += self.compute_files_size_by_type(filetype)
        for child in self.childs.all():
            if not self.childs.all():
                pass
            else:
                childs_num += child.compute_num_files_by_type(filetype)
        return childs_num

    def compute_total_size_subfolders(self):
        """Retorna tamaño total de la carpeta.

        Itera archivos contenidos en la carpeta y
        en sus subcarpetas para sumar el peso de
        los archivos en kb
        
        """
        childs_size= 0
        childs_size += self.compute_files_size()
        for child in self.childs.all():
            if not self.childs.all():
                pass
            else:
                childs_size += child.compute_total_size_subfolders()
        return childs_size

    def return_folder_contain(self):
        """Retorna archivos contenidos.

        Itera archivos contenidos y regresa los nombres
        en una lista
        
        """
        estructure = []
        for file in self.files.all():
            estructure.append(file.name)
        return estructure

    def compute_estructure_subfolders(self):
        """Retorna la estructura de subcarpetas.

        Itera carpetas hijas para retornar en un
        diccionario los ficheros contenidos y subcarpetas
        
        """
        estructure = self.return_folder_contain()
        for child in self.childs.all():
            if not self.childs.all():
                pass
            else:
                estructure.append({ child.name  : child.compute_estructure_subfolders()})
        return estructure