from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save

# Create your models here.


class Disciplina(models.Model):
   nome = models.CharField(max_length=70)
   criado_em = models.DateTimeField(blank=True, null=True, auto_now_add=True)

   def __str__(self):
      return self.nome


class Curso(models.Model):
   nome = models.CharField(max_length=50)
   disciplinas = models.ManyToManyField(Disciplina, through='CursoDisciplina')
   criado_em = models.DateTimeField(blank=True, null=True, auto_now_add=True)

   def __str__(self):
      return self.nome


class CursoDisciplina(models.Model):
   curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)
   disciplina = models.ForeignKey(Disciplina, on_delete=models.DO_NOTHING)

   def __str__(self):
      return self.curso.nome + ' - ' + self.disciplina.nome


class Aluno(models.Model):
   nome = models.CharField(max_length=200)
   registro_academico = models.CharField(max_length=10)
   data_nascimento = models.DateField()
   curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)
   disciplinas = models.ManyToManyField(CursoDisciplina, related_name='alunos')
   foto = models.ImageField()
   criado_em = models.DateTimeField(blank=True, null=True, auto_now_add=True)

   def __str__(self):
      return self.nome


class Professor(models.Model):
   nome_completo = models.CharField(max_length=200)
   cpf = models.CharField(max_length=11)
   data_nascimento = models.DateField(blank=True, null=True)
   curso_disciplinas = models.ManyToManyField(CursoDisciplina, related_name='professores')
   criado_em = models.DateTimeField(blank=True, null=True, auto_now_add=True)
   user = models.OneToOneField(User, related_name='professor', on_delete=models.DO_NOTHING)

   def __str__(self):
      return self.nome_completo


class Aula(models.Model):
   descricao = models.CharField(max_length=100)
   data = models.DateTimeField()
   chamada_iniciada = models.DateTimeField(blank=True, null=True)
   chamada_finalizada = models.DateTimeField(blank=True, null=True)
   curso_disciplina = models.ForeignKey(CursoDisciplina, related_name='aulas', on_delete=models.CASCADE)
   criado_em = models.DateTimeField(blank=True, null=True, auto_now_add=True)
   alunos = models.ManyToManyField(Aluno, through='AulaAluno')
   ativo = models.BooleanField(default=True)

   def __str__(self):
      return self.descricao


class AulaAluno(models.Model):
   aluno = models.ForeignKey(Aluno, on_delete=models.DO_NOTHING, related_name='aulas')
   aula = models.ForeignKey(Aula, on_delete=models.DO_NOTHING)
   presente = models.BooleanField(default=False)
   horario_presenca = models.DateTimeField(blank=True, null=True)

@receiver(post_save, sender=Aula)
def add_alunos(sender, **kwargs):
   aula = kwargs['instance']
   if len(aula.alunos.all()) == 0:
      alunos = aula.curso_disciplina.alunos.all()
      for aluno in alunos:
         AulaAluno(aluno_id=aluno.id, aula_id=aula.id).save()
