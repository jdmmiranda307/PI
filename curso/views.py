import subprocess
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from core.models import Curso, CursoDisciplina, Disciplina, Professor
from datetime import datetime



@login_required
def curso_index(request):
    if request.method == 'GET':
        return render(request, 'cursos.html')
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
                    curso = Curso.objects.get(id=data.pop('id')[0])
                    for key in data.keys():
                        if key != 'disciplinas' and data[key]:
                            setattr(curso, key, data[key])
                        else:
                            for d_id in disciplinas_removidas:
                                cds = CursoDisciplina.objects.filter(curso_id=curso.id, disciplina_id=d_id)
                                for cd in cds:
                                    cd.delete()
                            current_ids = curso.disciplinas.all().values_list('id')
                            current_ids = [ps[0] for ps in current_ids]
                            inativos_ids = curso.disciplinas.filter(cursodisciplina__ativo=False).values_list('id')
                            inativos_ids = [ps[0] for ps in inativos_ids]
                            for disciplina in data['disciplinas']:
                                if int(disciplina) not in current_ids:
                                    cd = CursoDisciplina(curso_id=curso.id, disciplina_id=disciplina)
                                    cd.save()
                                elif int(disciplina) in inativos_ids:
                                    cd = CursoDisciplina.objects.filter(disciplina_id=disciplina, curso_id=curso.id)[0]
                                    cd.ativo = True
                                    cd.save()
                    curso.save()
                    return HttpResponse(status=204)
                except:
                    return HttpResponse(status=400)
            else:
                try:
                    curso = Curso()
                    for key in data.keys():
                        if key != 'disciplinas' and data[key]:
                            setattr(curso, key, data[key])
                    curso.save()
                    for disciplina in data['disciplinas']:
                        cd = CursoDisciplina(curso_id=curso.id, disciplina_id=disciplina)
                        cd.save()
                    curso.save()
                    return HttpResponse(status=200)
                except:
                    return HttpResponse(status=400)
        except:
            return HttpResponse(status=500)


@login_required
def get_cursos(request):
    cursos = Curso.objects.all().filter(ativo=True)
    return JsonResponse(cursos_dict(cursos))


@login_required
def get_curso(request, id_curso):
    curso = Curso.objects.filter(id=id_curso)
    return JsonResponse(cursos_dict(curso))


def cursos_dict(cursos):
    data = {}
    data_list = []
    for curso in cursos:
        current_dict = {}
        current_dict['id'] = curso.id
        current_dict['nome'] = curso.nome
        disciplinas = [disciplina.nome for disciplina in curso.disciplinas.filter(cursodisciplina__ativo=True)]
        current_dict['disciplinas_id'] = [disciplina.id for disciplina in curso.disciplinas.filter(cursodisciplina__ativo=True)]
        data_list.append(current_dict)
    data['cursos'] = data_list
    return data


@login_required
def get_curso_disciplinas(request):
    if request.user.is_superuser:
        curso_disciplinas = CursoDisciplina.objects.all().filter(ativo=True)
    else:
        curso_disciplinas = request.user.professor.curso_disciplinas.all()
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


@login_required
def curso(request, id_curso):
    if request.method == 'GET':
        curso = Curso.objects.get(pk=id_curso)
        return render(request, 'curso.html', {'curso': curso})


@login_required
def create_curso(request):
    if request.method == 'GET':
        return render(request, 'curso.html')


def delete_curso(request, id_curso):
    try:
        curso = Curso.objects.get(id=id_curso)
        curso.delete()
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)

@login_required
def get_disciplinas_professor(request, id_professor):
    disciplinas = list(CursoDisciplina.objects.filter(professores__id=id_professor).filter(ativo=True))
    return JsonResponse(curso_disciplinas_dict(disciplinas))