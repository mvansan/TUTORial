# Generated by Django 4.2.2 on 2023-08-31 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_merge_20230830_1845'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('email', models.EmailField(max_length=200)),
            ],
            options={
                'db_table': 'contacts',
            },
        ),
        migrations.AddField(
            model_name='matching',
            name='matching_count',
            field=models.IntegerField(default=0),
        ),
    ]