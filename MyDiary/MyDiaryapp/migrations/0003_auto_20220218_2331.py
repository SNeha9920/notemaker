# Generated by Django 3.1.6 on 2022-02-18 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyDiaryapp', '0002_tokens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journals',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
