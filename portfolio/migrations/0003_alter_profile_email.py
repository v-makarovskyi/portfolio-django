# Generated by Django 4.1.1 on 2022-11-25 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0002_alter_post_headline_alter_post_thumbnail_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="email",
            field=models.EmailField(max_length=200, unique=True),
        ),
    ]