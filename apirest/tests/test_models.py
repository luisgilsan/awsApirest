import pytest


@pytest.mark.django_db


class TestMyModel:
    def test_mymodel(self):
        my_model = mixer.blend("folders.Folder")
        assert my_model.pk == 1, "Should create a MyModel instance"