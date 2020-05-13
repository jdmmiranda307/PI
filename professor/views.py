import json
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from core.models import Professor, CursoDisciplina
from datetime import datetime


# Create your views here.
@login_required
def professor_index(request):
    if request.method == 'GET':
        return render(request, 'professores.html')
    elif request.method == 'POST':
        try:
            data = dict(request.POST)
            data = {key:value[0] for (key,value) in data.items()}
            disciplinas_removidas = ''
            if data.get('disciplinas_removidas', False):
                disciplinas_removidas = data.pop('disciplinas_removidas').split(',')
            data['disciplinas'] = data['disciplinas'].split(',')
            user_data = {}
            user_data['email'] = data.pop('email')
            is_superuser = data.pop('is_superuser')
            is_superuser = True if is_superuser == 'true' else False
            user_data['is_superuser'] = is_superuser
            if data.get('id', False):
                try:
                    professor = Professor.objects.get(id=data.pop('id')[0])
                    user = professor.user
                    if user_data['email'] != user.email:
                        if User.objects.filter(email=user_data['email']).count() != 0:
                            return HttpResponse(status=406)
                    for key in user_data.keys():
                        setattr(user, key, user_data[key])
                    user.save()
                    for key in data.keys():
                        if key != 'disciplinas' and data[key]:
                            setattr(professor, key, data[key])
                        else:
                            for d_id in disciplinas_removidas:
                                professor.curso_disciplinas.remove(CursoDisciplina.objects.get(id=d_id))
                            current_ids = professor.curso_disciplinas.all().values_list('id')
                            current_ids = [ps[0] for ps in current_ids]
                            for disciplina in data['disciplinas']:
                                if int(disciplina) not in current_ids:
                                    professor.curso_disciplinas.add(CursoDisciplina.objects.get(id=disciplina))
                    professor.save()
                    return HttpResponse(status=204)
                except:
                    return HttpResponse(status=400)
            else:
                if User.objects.filter(email=user_data['email']).count() == 0:
                    user = User()
                    try:
                        user.email = user_data['email']
                        user.username = user_data['email']
                        user.is_superuser = user_data['is_superuser']
                        user.set_password(user_data['email'])
                        user.save()
                        professor = Professor()
                        for key in data.keys():
                            if key != 'disciplinas' and data[key]:
                                setattr(professor, key, data[key])
                        professor.user = user
                        professor.save()
                        for disciplina in data['disciplinas']:
                            professor.curso_disciplinas.add(CursoDisciplina.objects.get(id=disciplina))
                        professor.save()
                        return HttpResponse(status=200)
                    except:
                        user.delete()
                        return HttpResponse(status=400)
                else:
                    return HttpResponse(status=406)
        except:
            return HttpResponse(status=500)


@login_required
def get_professores(request):
    professores = Professor.objects.all()
    return JsonResponse(professores_dict(professores))


@login_required
def get_professor(request, id_professor):
    professor = Professor.objects.filter(id=id_professor)
    return JsonResponse(professores_dict(professor))


@login_required
def professor(request, id_professor):
    if request.method == 'GET':
        professor = Professor.objects.get(pk=id_professor)
        return render(request, 'professor.html', {'professor': professor})


@login_required
def minhas_informacoes(request, id_professor):
    if request.method == "GET":
        professor = Professor.objects.get(id=id_professor)
        return render(request, 'minhas-informacoes.html', {'professor': professor})
    elif request.method == 'POST':
        try:
            data = dict(request.POST)
            data = {key:value[0] for (key,value) in data.items()}
            user_data = {}
            user_data['email'] = data.pop('email')
            user_data['password'] = data.pop('password')
            try:
                professor = Professor.objects.get(id=id_professor)
                for key in data.keys():
                    setattr(professor, key, data[key])
                professor.save()
                user = professor.user
                if user_data['email'] != user.email:
                    if User.objects.filter(email=user_data['email']).count() != 0:
                        return HttpResponse(status=406)
                user.set_password(user_data['password'])
                user.email = user_data['email']
                user.username = user_data['email']
                user.save()
                update_session_auth_hash(request, user)
                return HttpResponse(status=204)
            except:
                return HttpResponse(status=400)
        except:
            return HttpResponse(status=500)

@login_required
def create_professor(request):
    if request.method == 'GET':
        return render(request, 'professor.html')


def delete_professor(request, id_professor):
    try:
        professor = Professor.objects.get(id=id_professor)
        professor.delete()
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)


@login_required
def get_professores_disciplina(request, id_disciplina):
    professores = list(CursoDisciplina.objects.get(id=id_disciplina).professores.all())
    if request.user.professor in professores and\
      professores.index(request.user.professor) != 0:
        professores.pop(request.user.professor)
        professores.insert(request.user.professor, 0)
    return JsonResponse(professores_dict(professores))



def professores_dict(professores):
    data = {}
    data_list = []
    for professor in professores:
        current_dict = {}
        current_dict['id'] = professor.id
        current_dict['nome'] = professor.nome_completo
        current_dict['cpf'] = professor.cpf
        current_dict['data_nascimento'] = professor.data_nascimento
        cursos = [record.curso.nome for record in professor.curso_disciplinas.all()]
        cursos = list(dict.fromkeys(cursos))
        current_dict['cursos'] = ', '.join(cursos)
        disciplinas = [disciplina.__str__() for disciplina in professor.curso_disciplinas.all()]
        current_dict['disciplinas_id'] = [disciplina.id for disciplina in professor.curso_disciplinas.all()]
        current_dict['email'] = professor.user.email
        current_dict['administrador'] = professor.user.is_superuser
        data_list.append(current_dict)
    data['professores'] = data_list
    return data
