# Generated by Django 4.0.5 on 2023-02-03 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='StudyPal\x08ase\\static\\images\x07vatar.png', null=True, upload_to=''),
        ),
    ]