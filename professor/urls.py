from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.professor_index, name='professores'),
    url(r'^get-professores$', views.get_professores, name='get-professores'),
    url(r'^create-professor$', views.create_professor, name='create-professor'),
    url(r'^get-professor/(?P<id_professor>[\w]+)$', views.get_professor, name='get-professor'),
    url(r'^(?P<id_professor>[\w]+)$', views.professor, name='professor'),
    url(r'^delete-professor/(?P<id_professor>[\w]+)$', views.delete_professor, name='delete-professor'),
    url(r'^minhas-informacoes/(?P<id_professor>[\w]+)$', views.minhas_informacoes, name='minhas-informacoes')
]
