# Generated by Django 5.1.1 on 2024-09-22 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admision', '0004_remove_eps_paciente_estado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paciente',
            name='numero_identificacion',
        ),
        migrations.AddField(
            model_name='eps_paciente',
            name='estado',
            field=models.CharField(choices=[('activo', 'Usuario Activo'), ('inactivo', 'Usuario Inactivo'), ('bloqueado', 'Usuario Bloqueado')], default='activo', max_length=20),
        ),
        migrations.AlterField(
            model_name='eps',
            name='nombre_eps',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='apellido_paciente',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nombre_paciente',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='telefono_paciente',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='tipo_identificacion',
            field=models.CharField(max_length=100),
        ),
    ]
