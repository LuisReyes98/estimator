import json

from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class SessionVariablesAPI(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Get el valor de la variable de sesion del nombre del url
        variable_name = self.kwargs['session_var']
        response = ""
        if variable_name in request.session:
            response = request.session[variable_name]
        return JsonResponse({'value': response})

    def post(self, request, *args, **kwargs):
        # set la variable de sesion del nombre del url
        value = json.loads(request.body)['value']
        variable_name = self.kwargs['session_var']
        request.session[variable_name] = value
        return HttpResponse(200)
