from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.disciplina_index, name='disciplinas'),
    url(r'^get-disciplinas$', views.get_disciplinas, name='get-disciplinas'),
    # url(r'^disciplina/(?P<id_disciplina>[\w]+)$', views.disciplina, name='disciplina'),
    # url('add', views.add_disciplina),
]
