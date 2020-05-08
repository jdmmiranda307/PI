from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.disciplina_index, name='disciplinas'),
    url(r'^get-disciplinas$', views.get_disciplinas, name='get-disciplinas'),
    url(r'^create-disciplina$', views.create_disciplina, name='create-disciplina'),
    url(r'^get-disciplina/(?P<id_disciplina>[\w]+)$', views.get_disciplina, name='get-disciplina'),
    url(r'^(?P<id_disciplina>[\w]+)$', views.disciplina, name='disciplina'),
    url(r'^delete-disciplina/(?P<id_disciplina>[\w]+)$', views.delete_disciplina, name='delete-disciplina')
]
