from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.curso_index, name='cursos'),
    url(r'^get-cursos$', views.get_cursos, name='get-cursos'),
    url(r'^get-curso-disciplinas$', views.get_curso_disciplinas, name='get-cursos-disciplinas'),
    url(r'^create-curso$', views.create_curso, name='create-curso'),
    url(r'^get-curso/(?P<id_curso>[\w]+)$', views.get_curso, name='get-curso'),
    url(r'^(?P<id_curso>[\w]+)$', views.curso, name='curso'),
    url(r'^delete-curso/(?P<id_curso>[\w]+)$', views.delete_curso, name='delete-curso')
]
