# Generated by Django 4.2.6 on 2023-10-16 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_data', '0002_route_stop_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='tdx_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='tdx_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddIndex(
            model_name='route',
            index=models.Index(fields=['tdx_id', 'direction'], name='bus_data_ro_tdx_id_9d3f13_idx'),
        ),
        migrations.AddIndex(
            model_name='stop',
            index=models.Index(fields=['tdx_id'], name='bus_data_st_tdx_id_592a4e_idx'),
        ),
    ]