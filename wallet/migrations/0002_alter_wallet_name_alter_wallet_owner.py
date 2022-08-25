# Generated by Django 4.1 on 2022-08-23 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wallet", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="name",
            field=models.CharField(
                default="1783E6C3",
                editable=False,
                max_length=8,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="wallet",
            name="owner",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
