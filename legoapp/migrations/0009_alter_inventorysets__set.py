# Generated by Django 4.1.4 on 2022-12-19 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legoapp', '0008_alter_inventoryminifigs_inventory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorysets',
            name='_set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='legoapp.set'),
        ),
    ]
