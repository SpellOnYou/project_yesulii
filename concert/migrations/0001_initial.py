# Generated by Django 3.2.5 on 2021-08-04 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConcertList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='제목', max_length=200)),
                ('date', models.DateField(help_text='일자')),
                ('time', models.TimeField(blank=True, help_text='시간', null=True)),
                ('link', models.URLField(help_text='링크')),
                ('place', models.CharField(help_text='장소', max_length=200)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
