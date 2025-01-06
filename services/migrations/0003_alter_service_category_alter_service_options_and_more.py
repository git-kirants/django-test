# Generated by Django 5.1.4 on 2025-01-06 15:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('lawn_care', 'Lawn Care'), ('landscaping', 'Landscaping'), ('tree_service', 'Tree Service'), ('garden_design', 'Garden Design'), ('maintenance', 'Garden Maintenance'), ('pest_control', 'Pest Control')], max_length=20),
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='service',
            name='duration',
            field=models.PositiveIntegerField(help_text='Duration in minutes'),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='service',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
