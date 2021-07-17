from django.test import TestCase
from .models import Folder,File
# Create your tests here.
class FolderTetstCase(TestCase):
    """ Define las pruebas unitarias de la app folders """
    
    def test_create_folder(self):
        """
            Prueba creado de carpeta.
        """
        Folder.objects.create(name='folderTests',
            category=None,
            parent=None)
        self.assertEqual(Folder.objects.count(),1)

    def test_delete_folder_no_empty(self):
        """
            Prueba borrado de folder con subcarpetas y archivos.
        """
        folder = Folder.objects.create(name='folderTests',
            category=None,
            parent=None)
        File.objects.create(
            name='fileTets',
            folder=folder,
            path='/c',
            file_type_id=None,
            lines=0,
            size_in_kb=0
        )
        Folder.objects.create(name='folderTestsChild',
            category=None,
            parent=folder)
        folder.delete()
        self.assertEqual(Folder.objects.count(),2)

    def test_delete_folder_empty(self):
        """
            Prueba borrador de archivo vacio.
        """
        folder = Folder.objects.create(name='folderTests',
            category=None,
            parent=None)
        folder.delete()
        self.assertEqual(Folder.objects.count(),0)

    def test_create_file(self):
        """
            Prueba creacion de archivo.
        """
        folder = Folder.objects.create(name='folderTests',
            category=None,
            parent=None)
        File.objects.create(
            name='fileTets',
            folder=folder,
            path='/c',
            file_type_id=None,
            lines=0,
            size_in_kb=0
        )
        self.assertEqual(File.objects.count(),1)
