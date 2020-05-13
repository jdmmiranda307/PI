from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.aula_index, name='aulas'),
    url(r'^get-aulas$', views.get_aulas, name='get-aulas'),
    url(r'^get-aula/(?P<id_aula>[\w]+)$$', views.get_aula, name='get-aula'),
    url(r'^aula/(?P<id_aula>[\w]+)$', views.aula, name='aula'),
    url(r'^create-aula/', views.create_aula, name='create-aula'),
    url(r'^(?P<id_aula>[\w]+)$', views.aula_dados, name='aula_dados'),
    url(r'^start/(?P<id_aula>[\w]+)$', views.start_aula, name='start-aula'),
    url(r'^end/(?P<id_aula>[\w]+)$', views.end_aula, name='end-aula'),
    url(r'^get-alunos/(?P<id_aula>[\w]+)$', views.alunos, name='get-alunos'),
    url(r'^status-aula/(?P<id_aula>[\w]+)$', views.status_aula, name='status-aula'),
    url(r'^change-status-aula-aluno/(?P<id_aula>[\w]+)/(?P<id_aluno>[\w]+)$', views.change_status_aula_aluno, name='change-status-aula-aluno'),
]
