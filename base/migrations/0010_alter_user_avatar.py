# Generated by Django 3.2.20 on 2024-04-16 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='static/images/avatar.png', null=True, upload_to=''),
        ),
    ]
