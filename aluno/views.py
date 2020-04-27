import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from core.models import Aluno, CursoDisciplina
from datetime import datetime


@login_required
def aluno_index(request):
    if request.method == 'GET':
        return render(request, 'alunos.html')
    elif request.method == 'POST':
        try:
            data = dict(request.POST)
            data = {key:value[0] for (key,value) in data.items()}
            disciplinas_removidas = ''
            if data.get('disciplinas_removidas', False):
                disciplinas_removidas = data.pop('disciplinas_removidas').split(',')
            data['disciplinas'] = data['disciplinas'].split(',')
            if data.get('id', False):
                try:
                    aluno = Aluno.objects.get(id=data.pop('id')[0])
                    for key in data.keys():
                        if key != 'disciplinas' and data[key]:
                            setattr(aluno, key, data[key])
                        else:
                            for d_id in disciplinas_removidas:
                                aluno.disciplinas.remove(CursoDisciplina.objects.get(id=d_id))
                            current_ids = aluno.disciplinas.all().values_list('id')
                            current_ids = [ps[0] for ps in current_ids]
                            for disciplina in data['disciplinas']:
                                if int(disciplina) not in current_ids:
                                    aluno.disciplinas.add(CursoDisciplina.objects.get(id=disciplina))
                    if 'foto' in request.FILES.keys():
                        aluno.foto = request.FILES['foto']
                    aluno.save()
                    return HttpResponse(status=204)
                except:
                    return HttpResponse(status=400)
            else:
                try:
                    aluno = Aluno()
                    for key in data.keys():
                        if key != 'disciplinas' and data[key]:
                            setattr(aluno, key, data[key])
                    aluno.save()
                    for disciplina in data['disciplinas']:
                        aluno.disciplinas.add(CursoDisciplina.objects.get(id=disciplina))
                    if 'foto' in request.FILES.keys():
                        aluno.foto = request.FILES['foto']
                    aluno.save()
                    return HttpResponse(status=200)
                except:
                    return HttpResponse(status=400)
        except:
            return HttpResponse(status=500)


@login_required
def get_alunos(request):
    alunos = Aluno.objects.all()
    return JsonResponse(alunos_dict(alunos))


@login_required
def get_aluno(request, id_aluno):
    aluno = Aluno.objects.filter(id=id_aluno)
    return JsonResponse(alunos_dict(aluno))


@login_required
def aluno(request, id_aluno):
    if request.method == 'GET':
        aluno = Aluno.objects.get(pk=id_aluno)
        return render(request, 'aluno.html', {'aluno': aluno})


@login_required
def create_aluno(request):
    if request.method == 'GET':
        return render(request, 'aluno.html')


def delete_aluno(request, id_aluno):
    try:
        aluno = Aluno.objects.get(id=id_aluno)
        aluno.delete()
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)


def alunos_dict(alunos):
    data = {}
    data_list = []
    for aluno in alunos:
        current_dict = {}
        current_dict['id'] = aluno.id
        current_dict['nome'] = aluno.nome
        current_dict['registro_academico'] = aluno.registro_academico
        current_dict['data_nascimento'] = aluno.data_nascimento
        current_dict['curso'] = aluno.curso.nome
        current_dict['curso_id'] = aluno.curso.id
        disciplinas = [disciplina.__str__() for disciplina in aluno.disciplinas.all()]
        current_dict['disciplinas_id'] = [disciplina.id for disciplina in aluno.disciplinas.all()]
        current_dict['disciplinas'] = ' - '.join(disciplinas)
        current_dict['foto'] = aluno.foto.url
        data_list.append(current_dict)
    data['alunos'] = data_list
    return data
