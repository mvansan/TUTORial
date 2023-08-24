# Generated by Django 4.2.4 on 2023-08-24 02:45

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_user_role_alter_matching_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='subtopic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.subtopic'),
        ),
        migrations.AlterField(
            model_name='matching',
            name='salary_max',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='matching',
            name='salary_min',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='matching',
            name='time',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, '月'), (2, '火'), (3, '水'), (4, '木'), (5, '金'), (6, '土'), (7, '日')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.topic'),
        ),
    ]
