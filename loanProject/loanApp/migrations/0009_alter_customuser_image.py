# Generated by Django 4.2.7 on 2023-12-14 23:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("loanApp", "0008_alter_customuser_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="image",
            field=models.FileField(blank=True, null=True, upload_to="images"),
        ),
    ]
