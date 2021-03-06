# Generated by Django 3.1.7 on 2021-03-06 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkConnectivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_from', models.IntegerField()),
                ('node_to', models.IntegerField()),
            ],
            options={
                'db_table': 'network_connectivity',
                'unique_together': {('node_from', 'node_to')},
            },
        ),
    ]
