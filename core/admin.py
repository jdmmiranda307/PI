from django.contrib import admin
from core.models import *

# Register your models here.
admin.site.register(Aluno)
admin.site.register(Aula)
admin.site.register(Curso)
admin.site.register(Disciplina)
admin.site.register(Professor)
admin.site.register(CursoDisciplina)
admin.site.register(AulaAluno)