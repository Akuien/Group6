# Generated by Django 4.2.7 on 2023-12-08 12:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("loanApp", "0003_rename_userdetails_userdetail"),
    ]

    operations = [
        migrations.AddField(
            model_name="applicant",
            name="loan_id",
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="risk_flag",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
