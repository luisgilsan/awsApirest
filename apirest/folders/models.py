from django.db import models
import os
from django.conf import settings
from pathlib import Path
import os 
from django.http import JsonResponse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# Create your models here.
class Folder(models.Model):

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

    def save(self, *args, **kwargs):
        new_folder = os.path.join(settings.MEDIA_ROOT, self.name)
        os.mkdir(new_folder)
        super(Folder, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print("bORRANDO FOLDER")
        if self.files.all() or self.childs():
            return JsonResponse({'Error':'El folder no se encuentra vacio'})
        else:
            super(Folder, self).delete(*args, **kwargs)

class FolderCategory(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='category_icons')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Folder Category'
        verbose_name_plural = 'Folder Categories'

class File(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    folder = models.ForeignKey("Folder", related_name='files',
        verbose_name="Folder", on_delete=models.CASCADE)
    path = models.CharField(max_length=255, verbose_name="Path")
    file_type_id = models.ForeignKey("FileType", related_name='files',
        blank=True,null=True, verbose_name="File Type", on_delete=models.SET_NULL)
    lines = models.IntegerField(verbose_name="Lines",default=0)
    size_in_kb = models.FloatField(verbose_name="Size (KB)",default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

class FileType(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='type_icons')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'