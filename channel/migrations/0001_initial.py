# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-07 01:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('season_number', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('netflix_id', models.CharField(blank=True, max_length=30)),
                ('wikipedia_url', models.CharField(blank=True, max_length=300)),
                ('seasons_total', models.IntegerField(blank=True, null=True)),
                ('episodes_total', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('netflix_id', models.CharField(blank=True, max_length=20)),
                ('media_type', models.CharField(choices=[('T', 'TV Episode'), ('M', 'Movie')], max_length=1)),
                ('episodeNum', models.IntegerField(blank=True, null=True)),
                ('year', models.CharField(blank=True, max_length=4, null=True)),
                ('runtime', models.IntegerField(blank=True, default=0, null=True)),
                ('season', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='channel.Season')),
            ],
        ),
        migrations.AddField(
            model_name='season',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Series'),
        ),
        migrations.AddField(
            model_name='channel',
            name='content',
            field=models.ManyToManyField(blank=True, to='channel.Video'),
        ),
    ]