# Generated by Django 4.0.6 on 2022-12-10 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_language_category_alter_language_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='description',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='language',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]