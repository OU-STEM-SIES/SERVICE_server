# Generated by Django 3.2.10 on 2022-01-13 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10)),
                ('rowsToDisplay', models.PositiveIntegerField(blank=True, choices=[(3, '3'), (6, '6'), (9, '9'), (15, '15'), (30, '30'), (100, '100'), (250, '250'), (500, '500'), (99999, 'All (slow)')], default=6)),
                ('gotoPage', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
