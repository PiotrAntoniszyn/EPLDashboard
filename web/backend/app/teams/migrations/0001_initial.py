# Generated by Django 3.2.3 on 2021-05-27 19:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=120)),
                ("last_name", models.CharField(max_length=120)),
                ("age", models.IntegerField()),
                ("position", models.CharField(max_length=20)),
                ("nationality", models.CharField(max_length=120)),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="teams.team"
                    ),
                ),
            ],
        ),
    ]