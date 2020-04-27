import subprocess
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from core.models import Disciplina
from datetime import datetime


# @login_required
# def aluno_index(request):
#     return render(request, 'alunos.html')


@login_required
def get_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return JsonResponse(disciplinas_dict(disciplinas))

# @login_required
# def aluno(request, id_aluno):
#     if request.method == 'GET':
#         aluno = Aluno.objects.get(pk=id_aluno)
#         return render(request, 'aluno.html', {'aluno': aluno})


def disciplinas_dict(disciplinas):
    data = {}
    data_list = []
    for disciplina in disciplinas:
        current_dict = {}
        current_dict['id'] = disciplina.id
        current_dict['nome'] = disciplina.nome
        data_list.append(current_dict)
    data['disciplinas'] = data_list
    return data
