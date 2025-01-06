# Generated by Django 5.1.4 on 2025-01-06 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_available_hours_user_company_website_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='providerapplication',
            options={'ordering': ['-submitted_at']},
        ),
        migrations.AddField(
            model_name='providerapplication',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='providerapplication',
            name='experience_years',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='providerapplication',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
