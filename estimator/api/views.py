import json

from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class SessionVariablesView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Code for GET requests
        variable_name = self.kwargs['session_var']
        return JsonResponse({'foo': variable_name})

    def post(self, request, *args, **kwargs):
        # Code for POST requests
        variable_name = self.kwargs['session_var']
        print(variable_name)
        received_json_data = json.loads(request.body)
        print(received_json_data)
