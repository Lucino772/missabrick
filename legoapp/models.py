from django.db import models

class Theme(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    parent = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)

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

    part_category = models.ForeignKey(PartsCategory, on_delete=models.SET_NULL, null=True)

class PartsRelationship(models.Model):
    id = models.AutoField(primary_key=True)
    rel_type = models.CharField(max_length=10)

    child_part = models.ForeignKey(Part, on_delete=models.SET_NULL, related_name='child', null=True)
    parent_part = models.ForeignKey(Part, on_delete=models.SET_NULL, related_name='parent', null=True)

class Element(models.Model):
    element_id = models.IntegerField(primary_key=True)

    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    part = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True)

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

    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)

class Inventory(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.IntegerField()
    is_minifig = models.BooleanField()

    _set = models.ForeignKey(Set, on_delete=models.SET_NULL, null=True)
    minifig = models.ForeignKey(Minifig, on_delete=models.SET_NULL, null=True)

class InventoryMinifigs(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()

    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    minifig = models.ForeignKey(Minifig, on_delete=models.SET_NULL, null=True)

class InventoryParts(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    is_spare = models.BooleanField()
    img_url = models.URLField()

    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    part = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)

class InventorySets(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()

    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    _set = models.ForeignKey(Set, on_delete=models.SET_NULL, null=True)

