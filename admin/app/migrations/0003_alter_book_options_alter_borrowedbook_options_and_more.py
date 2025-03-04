# Generated by Django 4.2.19 on 2025-02-22 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_book_isbn'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ('-date_created',)},
        ),
        migrations.AlterModelOptions(
            name='borrowedbook',
            options={'ordering': ('-date_created',)},
        ),
        migrations.AlterField(
            model_name='borrowedbook',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
