# Generated by Django 4.1.4 on 2022-12-20 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legoapp', '0010_alter_partsrelationship_child_part_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.color'),
        ),
        migrations.AlterField(
            model_name='element',
            name='part',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.part'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='_set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.set'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='minifig',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.minifig'),
        ),
        migrations.AlterField(
            model_name='inventoryminifigs',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.inventory'),
        ),
        migrations.AlterField(
            model_name='inventoryminifigs',
            name='minifig',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.minifig'),
        ),
        migrations.AlterField(
            model_name='inventoryparts',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.color'),
        ),
        migrations.AlterField(
            model_name='inventoryparts',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.inventory'),
        ),
        migrations.AlterField(
            model_name='inventoryparts',
            name='part',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.part'),
        ),
        migrations.AlterField(
            model_name='inventorysets',
            name='_set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.set'),
        ),
        migrations.AlterField(
            model_name='inventorysets',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.inventory'),
        ),
        migrations.AlterField(
            model_name='part',
            name='part_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.partscategory'),
        ),
        migrations.AlterField(
            model_name='partsrelationship',
            name='child_part',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='legoapp.part'),
        ),
        migrations.AlterField(
            model_name='partsrelationship',
            name='parent_part',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent', to='legoapp.part'),
        ),
        migrations.AlterField(
            model_name='set',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.theme'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legoapp.theme'),
        ),
    ]
