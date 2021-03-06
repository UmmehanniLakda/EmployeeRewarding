# Generated by Django 3.1.2 on 2021-10-29 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Client', '0003_project_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=0)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='Client.emp')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='Client.team')),
            ],
        ),
        migrations.CreateModel(
            name='Votechecksum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checksum', models.IntegerField(default=0)),
                ('team', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Client.team')),
            ],
        ),
    ]
