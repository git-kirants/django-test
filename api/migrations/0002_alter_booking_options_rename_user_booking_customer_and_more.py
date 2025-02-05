# Generated by Django 5.1.4 on 2025-01-06 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='user',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='notes',
            new_name='special_requests',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='booking_time',
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
    ]
