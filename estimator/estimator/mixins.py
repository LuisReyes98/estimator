from django.db import models

# Base Abstract model


class TimeStampFields(models.Model):
    """
        Modelo base para heredar y no tener que agregar los campos
        de creacion y edicion pero al ser abstracto su comportamiento
        es mas de mixin ya que no pueder representas la clase padre
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
