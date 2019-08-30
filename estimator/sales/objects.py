

class Prediction():
    """ Clase para manejar las predicciones antes de ser enviadas a las vistas """
    name = 'Prediction'

    def __init__(self, date='', pk=0):
        self.date = date
        self.pk = pk
