# Generated by Django 4.0.6 on 2022-08-05 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_friend_chat_messages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='chat_messages',
        ),
    ]
