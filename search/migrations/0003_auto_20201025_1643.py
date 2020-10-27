# Generated by Django 3.1.2 on 2020-10-25 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0003_userprofile_age'),
        ('search', '0002_auto_20201022_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationhistory',
            name='donated_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterUniqueTogether(
            name='donationrequest',
            unique_together={('sender', 'receiver')},
        ),
    ]