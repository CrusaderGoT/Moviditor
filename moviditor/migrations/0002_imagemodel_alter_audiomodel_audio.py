# Generated by Django 4.2.6 on 2023-10-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviditor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/\\images')),
            ],
        ),
        migrations.AlterField(
            model_name='audiomodel',
            name='audio',
            field=models.FileField(upload_to='media/\\audios'),
        ),
    ]
