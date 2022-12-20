# Generated by Django 4.1.4 on 2022-12-20 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legoapp', '0009_alter_inventorysets__set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partsrelationship',
            name='child_part',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='child', to='legoapp.part'),
        ),
        migrations.AlterField(
            model_name='partsrelationship',
            name='parent_part',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent', to='legoapp.part'),
        ),
    ]
