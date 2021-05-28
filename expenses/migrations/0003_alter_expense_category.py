# Generated by Django 3.2 on 2021-05-20 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_expense_ref_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('FOOD', 'FOOD'), ('RENT', 'RENT'), ('FEES', 'FEES'), ('OTHERS', 'OTHERS')], max_length=255),
        ),
    ]