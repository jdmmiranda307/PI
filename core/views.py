import json
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def login_caller(request):
    if request.method == "POST":
        try:
            data = request.body
            if type(data) == bytes:
                data = data.decode('utf8')
            data = json.loads(data)
            user = authenticate(username=data["username"], password=data["password"])
            if user:
                login(request, user)
                response = 200
            else:
                response = 400
        except Exception as e:
            response = 500
        return JsonResponse(status=response, data={'is_superuser': user.is_superuser})
    else:
        return render(request, 'login.html')