# Generated by Django 4.1.3 on 2022-11-09 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('complaintApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplaintMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('complaint', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress ', 'In Progress'), ('completed ', 'Completed')], default='pending', max_length=256)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaint_master_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complaint_master_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
