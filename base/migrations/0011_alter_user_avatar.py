# Generated by Django 3.2.20 on 2024-04-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.png', null=True, upload_to=''),
        ),
    ]