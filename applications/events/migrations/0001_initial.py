# Generated by Django 3.2 on 2022-01-01 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeStampModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('timestampmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.timestampmodel')),
                ('title', models.CharField(max_length=150, verbose_name='Job Title')),
                ('location', models.CharField(max_length=150, verbose_name='Location')),
                ('start_date', models.DateTimeField(blank=True, max_length=150, null=True, verbose_name='Start Date')),
                ('end_date', models.DateTimeField(blank=True, max_length=150, null=True, verbose_name='End Date')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Event Description')),
                ('banner', models.FileField(blank=True, null=True, upload_to='Event-Banners', verbose_name='Banners')),
                ('is_published', models.BooleanField(default=False, verbose_name='Published')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, verbose_name='Slug')),
                ('user_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Events',
                'verbose_name_plural': 'Events',
                'ordering': ('-created',),
            },
            bases=('events.timestampmodel',),
        ),
    ]
