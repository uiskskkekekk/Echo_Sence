# Generated by Django 5.1.4 on 2025-01-02 14:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('artist_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('url', models.URLField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'artist',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'category',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('music_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=20, null=True)),
                ('rating', models.IntegerField(default=0, null=True)),
                ('outer_url', models.URLField(blank=True, max_length=500, null=True)),
                ('rating_count', models.IntegerField(default=0)),
                ('listen_count', models.IntegerField(default=0)),
                ('features', models.JSONField()),
                ('artist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Music.artist')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Music.category')),
            ],
            options={
                'db_table': 'music',
                'managed': True,
            },
        ),
    ]