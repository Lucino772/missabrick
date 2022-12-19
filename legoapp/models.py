from django.db import models

class Theme(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    parent = models.ForeignKey('Theme', null=True, on_delete=models.DO_NOTHING)

class Color(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    rgb = models.CharField(max_length=20)
    is_trans = models.BooleanField()

class PartsCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class Part(models.Model):
    part_num = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    part_material = models.CharField(max_length=255)

    part_category = models.ForeignKey(PartsCategory, on_delete=models.DO_NOTHING)

class PartsRelationship(models.Model):
    id = models.AutoField(primary_key=True)
    rel_type = models.CharField(max_length=10)

    child_part = models.ForeignKey(Part, on_delete=models.DO_NOTHING, related_name='child')
    parent_part = models.ForeignKey(Part, on_delete=models.DO_NOTHING, related_name='parent')

class Element(models.Model):
    element_id = models.IntegerField(primary_key=True)

    color = models.ForeignKey(Color, on_delete=models.DO_NOTHING)
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING, null=True)

class Minifig(models.Model):
    fig_num = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    num_parts = models.IntegerField()
    img_url = models.URLField()

class Set(models.Model):
    set_num = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    num_parts = models.IntegerField()
    img_url = models.URLField()

    theme = models.ForeignKey(Theme, on_delete=models.DO_NOTHING)

class Inventory(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.IntegerField()
    is_minifig = models.BooleanField()

    _set = models.ForeignKey(Set, on_delete=models.DO_NOTHING, null=True)
    minifig = models.ForeignKey(Minifig, on_delete=models.DO_NOTHING, null=True)

class InventoryMinifigs(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()

    inventory = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING, null=True)
    minifig = models.ForeignKey(Minifig, on_delete=models.DO_NOTHING)

class InventoryParts(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    is_spare = models.BooleanField()
    img_url = models.URLField()

    inventory = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING, null=True)
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING)
    color = models.ForeignKey(Color, on_delete=models.DO_NOTHING)

class InventorySets(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()

    inventory = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING, null=True)
    _set = models.ForeignKey(Set, on_delete=models.DO_NOTHING, null=True)

