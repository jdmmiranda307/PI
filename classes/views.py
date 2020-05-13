import subprocess
from .forms import AlunoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from core.models import Aluno, Aula, AulaAluno
from datetime import datetime


@login_required
def aula_index(request):
    return render(request, 'list-classes.html')


@login_required
def get_aulas(request):
    aulas = []
    if request.user.is_superuser:
        professor = request.user.professor
        disciplinas = professor.curso_disciplinas.all()
        for disciplina in disciplinas:
            aulas += disciplina.aulas.all()
    else:
        aulas = request.user.professor.aulas.all()
    return JsonResponse(aulas_dict(aulas))


@login_required
def get_aula(request, id_aula):
    aula = Aula.objects.filter(id=id_aula)
    return JsonResponse(aulas_dict(aula))


@login_required
def create_aula(request):
    if request.method == 'GET':
        return render(request, 'create-aula.html')
    if request.method == 'POST':
        try:
            data = dict(request.POST)
            data = {key:value[0] for (key,value) in data.items()}
            if data.get('id', False):
                try:
                    aula = Aula.objects.get(id=data.pop('id')[0])
                    for key in data.keys():
                        setattr(aula, key, data[key])
                    aula.save()
                    return HttpResponse(status=200)
                except:
                    return HttpResponse(status=400)
            else:
                try:
                    aula = Aula()
                    for key in data.keys():
                        setattr(aula, key, data[key])
                    if 'professor_responsavel_id' not in data.keys():
                        aula.professor_responsavel = request.user.professor
                    aula.save()
                    return HttpResponse(status=200)
                except:
                    return HttpResponse(status=400)
        except:
            return HttpResponse(status=500)


@login_required
def aula_dados(request, id_aula):
    aula = Aula.objects.get(pk=id_aula)
    if request.method == 'GET':
        return render(request, 'create-aula.html', {'aula':aula})
    if request.method == 'POST':
        try:
            data = dict(request.POST)
            data = {key:value[0] for (key,value) in data.items()}
            try:
                aula = Aula()
                for key in data.keys():
                    setattr(aula, key, data[key])
                if 'professor_responsavel_id' not in data.keys():
                    aula.professor_responsavel = request.user.professor
                aula.save()
                return HttpResponse(status=200)
            except:
                return HttpResponse(status=400)
        except:
            return HttpResponse(status=500)


def aulas_dict(aulas):
    data = {}
    data_list = []
    for aula in aulas:
        current_dict = {}
        current_dict['id'] = aula.id
        current_dict['descricao'] = aula.descricao
        current_dict['curso_disciplina_id'] = aula.curso_disciplina.id
        current_dict['professor_responsavel_id'] = aula.professor_responsavel.id if aula.professor_responsavel else None
        current_dict['curso'] = aula.curso_disciplina.curso.nome
        current_dict['disciplina'] = aula.curso_disciplina.disciplina.nome
        current_dict['data'] = str(aula.data.day) + '/' + str(aula.data.month) + '/' + str(aula.data.year) + ' - ' + str(aula.data.time())
        current_dict['data_field'] = str(aula.data.year) + '-' + "{:02d}".format(aula.data.month) + '-' + "{:02d}".format(aula.data.day) + 'T' + str(aula.data.hour) + ':' + "{:02d}".format(aula.data.minute)
        current_dict['ativo'] = "Não" if aula.ativo else "Sim"
        data_list.append(current_dict)
    data['aulas'] = data_list
    return data


@login_required
def aula(request, id_aula):
    aula = Aula.objects.get(pk=id_aula)
    aula_finalizada = (True if aula.chamada_finalizada else False)
    return render(request, 'aula.html', {'aula': aula, 'aula_finalizada': aula_finalizada})


@login_required
def alunos(request, id_aula):
    aula = Aula.objects.get(pk=id_aula)
    alunos = aula.alunos.all()
    alunos = [aluno.id for aluno in alunos]
    aula_alunos = AulaAluno.objects.filter(aula_id=id_aula, aluno_id__in=alunos)
    return JsonResponse(alunos_dict(aula_alunos))


def alunos_dict(aula_alunos):
    data = {}
    data_list = []
    for aula_aluno in aula_alunos:
        current_dict = {}
        current_dict['id'] = aula_aluno.id
        current_dict['foto'] = aula_aluno.aluno.foto.url
        current_dict['nome'] = aula_aluno.aluno.nome
        current_dict['status'] = 'presente' if aula_aluno.presente else 'ausente'
        data_list.append(current_dict)
    data['alunos'] = data_list
    return data


def add_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AlunoForm()

    return render(request, 'add.html', {'form': form})


def start_aula(request, id_aula):
    aula = Aula.objects.get(id=id_aula)
    aula.chamada_iniciada = datetime.now()
    aula.save()
    p = subprocess.Popen("python manage.py recognize " + id_aula, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return redirect('/aulas/aula/'+id_aula)


def end_aula(request, id_aula):
    aula = Aula.objects.get(pk=id_aula)
    aula.chamada_finalizada = datetime.now()
    aula.ativo = False
    aula.save()
    return redirect('/aulas/')


def get_alunos(request):
    alunos = Aluno.objects.all()
    json = serializers.serialize('json', alunos)
    return HttpResponse(json, content_type='application/json')


def status_aula(request, id_aula):
    aula = Aula.objects.get(id=id_aula)
    response_dict = {'button':''}
    if aula.chamada_iniciada and aula.ativo:
        response_dict['button'] = '<a href="/aulas/end/' + str(aula.id) + '" class="btn btn-danger btn-filter" data-target="cancelado">Finalizar Aula</a>'
    elif not aula.chamada_finalizada:
        response_dict['button'] = '<a href="/aulas/start/' + str(aula.id) + '" class="btn btn-success btn-filter" data-target="pagado">Iniciar Aula</a>'
    return JsonResponse(response_dict)

@login_required
def change_status_aula_aluno(request, id_aula, id_aluno):
    if request.method == 'POST':
        aula_aluno = AulaAluno.objects.filter(aula_id=id_aula).filter(id=id_aluno)
        if len(aula_aluno) == 1:
            aula_aluno = aula_aluno[0]
            aula_aluno.presente = not (aula_aluno.presente)
            aula_aluno.save()
            response = 200
        else:
            response = 400
        return HttpResponse(response)