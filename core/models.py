from django.db import models

# Create your models here.


class Disciplina(models.Model):
   nome = models.CharField(max_length=70)
   criado_em = models.DateTimeField(blank=True, null=True, auto_now_add=True)

   def __str__(self):
      return self.nome


class Curso(models.Model):
   nome = models.CharField(max_length=50)
   disciplinas = models.ManyToManyField(Disciplina, related_name='cursos')
   criado_em = models.DateTimeField(blank=True, null=True, auto_now_add=True)

   def __str__(self):
      return self.nome


class Aluno(models.Model):
   nome = models.CharField(max_length=200)
   registro_academico = models.CharField(max_length=10)
   data_nascimento = models.DateField()
   curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)
   foto = models.ImageField()
   criado_em = models.DateTimeField(blank=True, null=True, auto_now_add=True)

   def __str__(self):
      return self.nome


class Professor(models.Model):
   nome_completo = models.CharField(max_length=200)
   cpf = models.CharField(max_length=11)
   data_nascimento = models.DateField(blank=True, null=True)
   disciplinas = models.ManyToManyField(Disciplina, related_name='professores')
   criado_em = models.DateTimeField(blank=True, null=True, auto_now_add=True)

   def __str__(self):
      return self.nome_completo


class Aula(models.Model):
   descricao = models.CharField(max_length=30)
   data = models.DateTimeField()
   disciplina = models.ForeignKey(Disciplina, related_name='aulas', on_delete=models.CASCADE)
   criado_em = models.DateTimeField(blank=True, null=True, auto_now_add=True)
   alunos = models.ManyToManyField(Aluno, through='AulaAluno')
   ativo = models.BooleanField(default=False)

   def __str__(self):
      return self.descricao


class AulaAluno(models.Model):
   aluno = models.ForeignKey(Aluno, on_delete=models.DO_NOTHING)
   aula = models.ForeignKey(Aula, on_delete=models.DO_NOTHING)
   presente = models.BooleanField(default=False)
   horario_presenca = models.DateTimeField(blank=True, null=True)

