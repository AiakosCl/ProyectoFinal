# Generated by Django 4.2.6 on 2023-11-21 22:48

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArteNativo', '0005_productos_estadoproducto_carritoitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='Descripcion',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productos',
            name='IdProducto',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='productos',
            name='NombreProducto',
            field=models.CharField(default='Descripción corta', max_length=50),
        ),
        migrations.AlterField(
            model_name='productos',
            name='PrecioUnitario',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]