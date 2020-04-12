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
    professor = request.user.professor
    disciplinas = professor.curso_disciplinas.all()
    aulas = []
    for disciplina in disciplinas:
        aulas += disciplina.aulas.all()
    return JsonResponse(aulas_dict(aulas))


def aulas_dict(aulas):
    data = {}
    data_list = []
    for aula in aulas:
        current_dict = {}
        current_dict['id'] = aula.id
        current_dict['descricao'] = aula.descricao
        current_dict['curso'] = aula.curso_disciplina.curso.nome
        current_dict['disciplina'] = aula.curso_disciplina.disciplina.nome
        current_dict['data'] = str(aula.data.day) + '/' + str(aula.data.month) + '/' + str(aula.data.year) + ' - ' + str(aula.data.time())
        current_dict['ativo'] = "Não" if aula.ativo else "Sim"
        data_list.append(current_dict)
    data['aulas'] = data_list
    return data


@login_required
def aula(request, id_aula):
    aula = Aula.objects.get(pk=id_aula)
    return render(request, 'aula.html', {'aula': aula})


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
