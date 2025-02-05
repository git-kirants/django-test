# Generated by Django 5.1.4 on 2025-01-09 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_providerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='providerprofile',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='provider_logos/'),
        ),
        migrations.AlterField(
            model_name='providerprofile',
            name='business_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
