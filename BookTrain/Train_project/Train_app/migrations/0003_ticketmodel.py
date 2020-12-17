# Generated by Django 3.0.7 on 2020-09-08 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Train_app', '0002_auto_20200908_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Train_number', models.IntegerField()),
                ('Train_name', models.CharField(max_length=256)),
                ('Origin', models.CharField(max_length=100)),
                ('Destination', models.CharField(max_length=100)),
                ('origin_time', models.CharField(max_length=100)),
                ('destination_time', models.CharField(max_length=100)),
                ('Travel_time', models.CharField(max_length=100)),
                ('Date', models.CharField(max_length=100)),
                ('Day', models.CharField(max_length=100)),
                ('Class', models.CharField(max_length=100)),
                ('Price', models.CharField(max_length=100)),
                ('Status', models.CharField(max_length=100)),
            ],
        ),
    ]