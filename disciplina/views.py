import subprocess
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from core.models import Disciplina
from datetime import datetime


@login_required
def disciplina_index(request):
    if request.method == 'GET':
        return render(request, 'disciplinas.html')
    elif request.method == 'POST':
        try:
            data = dict(request.POST)
            data = {key:value[0] for (key,value) in data.items()}
            if data.get('id', False):
                try:
                    disciplina = Disciplina.objects.get(id=data.pop('id')[0])
                    for key in data.keys():
                        setattr(disciplina, key, data[key])
                    disciplina.save()
                    return HttpResponse(status=204)
                except:
                    return HttpResponse(status=400)
            else:
                try:
                    disciplina = Disciplina()
                    for key in data.keys():
                        if key != 'disciplinas' and data[key]:
                            setattr(disciplina, key, data[key])
                    disciplina.save()
                    return HttpResponse(status=200)
                except:
                    return HttpResponse(status=400)
        except:
            return HttpResponse(status=500)


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


@login_required
def get_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return JsonResponse(disciplinas_dict(disciplinas))


@login_required
def get_disciplina(request, id_disciplina):
    disciplina = Disciplina.objects.filter(id=id_disciplina)
    return JsonResponse(disciplinas_dict(disciplina))


@login_required
def disciplina(request, id_disciplina):
    if request.method == 'GET':
        disciplina = Disciplina.objects.get(pk=id_disciplina)
        return render(request, 'disciplina.html', {'disciplina': disciplina})


@login_required
def create_disciplina(request):
    if request.method == 'GET':
        return render(request, 'disciplina.html')


def delete_disciplina(request, id_disciplina):
    try:
        disciplina = Disciplina.objects.get(id=id_disciplina)
        disciplina.delete()
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)
