# Generated by Django 4.0.5 on 2023-02-02 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='StudyPal\\static\\images\\Screenshot (99).png', null=True, upload_to=''),
        ),
    ]
