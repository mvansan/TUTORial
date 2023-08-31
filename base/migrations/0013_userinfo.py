# Generated by Django 4.2.4 on 2023-08-30 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_merge_20230829_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('job', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('about_me', models.TextField()),
                ('meeting_app', models.CharField(max_length=100)),
            ],
        ),
    ]