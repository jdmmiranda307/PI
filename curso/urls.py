from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.curso_index, name='cursos'),
    url(r'^get-cursos$', views.get_cursos, name='get-cursos'),
    url(r'^get-curso-disciplinas$', views.get_curso_disciplinas, name='get-cursos-disciplinas'),
    # url(r'^curso/(?P<id_curso>[\w]+)$', views.curso, name='curso'),
    # url('add', views.add_curso),
]
