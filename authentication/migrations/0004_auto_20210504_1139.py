# Generated by Django 3.2 on 2021-05-04 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]