# Generated by Django 4.0.5 on 2022-07-31 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='https://studypaltonny.s3.amazonaws.com/images/dedsec.png', null=True, upload_to=''),
        ),
    ]