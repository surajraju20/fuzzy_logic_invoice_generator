# Generated by Django 3.1.7 on 2021-04-04 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_name', models.CharField(max_length=100)),
                ('acc_no', models.IntegerField()),
                ('ifsc', models.CharField(max_length=100)),
                ('pan', models.CharField(max_length=100)),
                ('bank_name', models.CharField(max_length=100)),
                ('phone_number', models.IntegerField()),
                ('email_id', models.EmailField(max_length=250)),
                ('t_location', models.CharField(max_length=100)),
            ],
        ),
    ]
