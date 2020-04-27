from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.aluno_index, name='alunos'),
    url(r'^create-aluno$', views.create_aluno, name='create-aluno'),
    url(r'^get-alunos$', views.get_alunos, name='get-alunos'),
    url(r'^get-aluno/(?P<id_aluno>[\w]+)$', views.get_aluno, name='get-aluno'),
    url(r'^(?P<id_aluno>[\w]+)$', views.aluno, name='aluno'),
    url(r'^delete-aluno/(?P<id_aluno>[\w]+)$', views.delete_aluno, name='delete-aluno'),
    # url('add', views.add_aluno),
]
