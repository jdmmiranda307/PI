# Generated by Django 2.0.6 on 2020-04-08 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('registro_academico', models.CharField(max_length=10)),
                ('data_nascimento', models.DateField()),
                ('foto', models.ImageField(upload_to='')),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=30)),
                ('data', models.DateTimeField()),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True)),
                ('ativo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AulaAluno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presente', models.BooleanField(default=False)),
                ('horario_presenca', models.DateTimeField(blank=True, null=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Aluno')),
                ('aula', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Aula')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=70)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=200)),
                ('cpf', models.CharField(max_length=11)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True)),
                ('disciplinas', models.ManyToManyField(related_name='professores', to='core.Disciplina')),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='disciplinas',
            field=models.ManyToManyField(related_name='cursos', to='core.Disciplina'),
        ),
        migrations.AddField(
            model_name='aula',
            name='alunos',
            field=models.ManyToManyField(through='core.AulaAluno', to='core.Aluno'),
        ),
        migrations.AddField(
            model_name='aula',
            name='disciplina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aulas', to='core.Disciplina'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Curso'),
        ),
    ]
