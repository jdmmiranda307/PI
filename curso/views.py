import subprocess
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from core.models import Curso, CursoDisciplina
from datetime import datetime


# @login_required
# def aluno_index(request):
#     return render(request, 'alunos.html')


@login_required
def get_cursos(request):
    cursos = Curso.objects.all()
    return JsonResponse(cursos_dict(cursos))

# @login_required
# def aluno(request, id_aluno):
#     if request.method == 'GET':
#         aluno = Aluno.objects.get(pk=id_aluno)
#         return render(request, 'aluno.html', {'aluno': aluno})


def cursos_dict(cursos):
    data = {}
    data_list = []
    for curso in cursos:
        current_dict = {}
        current_dict['id'] = curso.id
        current_dict['nome'] = curso.nome
        data_list.append(current_dict)
    data['cursos'] = data_list
    return data


@login_required
def get_curso_disciplinas(request):
    curso_disciplinas = CursoDisciplina.objects.all()
    return JsonResponse(curso_disciplinas_dict(curso_disciplinas))

def curso_disciplinas_dict(curso_disciplinas):
    data = {}
    data_list = []
    for curso_disciplina in curso_disciplinas:
        current_dict = {}
        current_dict['id'] = curso_disciplina.id
        current_dict['nome'] = curso_disciplina.__str__()
        data_list.append(current_dict)
    data['cursoDisciplinas'] = data_list
    return data