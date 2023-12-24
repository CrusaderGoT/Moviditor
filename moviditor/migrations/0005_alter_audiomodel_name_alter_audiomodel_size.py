# Generated by Django 4.2.6 on 2023-10-15 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviditor', '0004_alter_audiomodel_name_alter_audiomodel_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiomodel',
            name='name',
            field=models.CharField(auto_created=True, editable=False),
        ),
        migrations.AlterField(
            model_name='audiomodel',
            name='size',
            field=models.DecimalField(auto_created=True, decimal_places=2, editable=False, max_digits=10),
        ),
    ]