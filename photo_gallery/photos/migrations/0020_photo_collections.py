# Generated by Django 4.0.6 on 2022-08-14 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0019_alter_collection_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='collections',
            field=models.ManyToManyField(to='photos.collection'),
        ),
    ]
