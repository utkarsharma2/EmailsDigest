# Generated by Django 3.1.7 on 2021-03-20 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('duration', models.IntegerField(default=60)),
                ('distribution_list', models.CharField(max_length=5000)),
                ('forward_unique', models.BooleanField(default=True)),
                ('threshold', models.FloatField(default=0.1)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField(default='')),
                ('body', models.TextField(default='')),
                ('label', models.UUIDField()),
                ('is_sent', models.BooleanField(default=False)),
                ('is_leader', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emailsdigest.application')),
            ],
        ),
    ]
