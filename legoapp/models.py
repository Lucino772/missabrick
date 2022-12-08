from django.db import models

class Color(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    rgb = models.CharField(max_length=20)
    is_trans = models.BooleanField()

class Element(models.Model):
    element_id = models.IntegerField(primary_key=True)
    part_num = models.CharField(max_length=20)
    color_id = models.IntegerField()

class Inventory(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.IntegerField()
    set_num = models.CharField(max_length=20)

class InventoryMinifigs(models.Model):
    id = models.AutoField(primary_key=True)
    inventory_id = models.IntegerField()
    fig_num = models.CharField(max_length=20)
    quantity = models.IntegerField()

class InventoryParts(models.Model):
    id = models.AutoField(primary_key=True)
    inventory_id = models.IntegerField()
    part_num = models.CharField(max_length=20)
    color_id = models.IntegerField()
    quantity = models.IntegerField()
    is_spare = models.BooleanField()
    img_url = models.URLField()

class InventorySets(models.Model):
    id = models.AutoField(primary_key=True)
    inventory_id = models.IntegerField()
    set_num = models.CharField(max_length=20)
    quantity = models.IntegerField()

class Minifig(models.Model):
    fig_num = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    num_parts = models.IntegerField()
    img_url = models.URLField()

class PartsCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class PartsRelationship(models.Model):
    id = models.AutoField(primary_key=True)
    rel_type = models.CharField(max_length=10)
    child_part_num = models.CharField(max_length=20)
    parent_part_num = models.CharField(max_length=20)

class Part(models.Model):
    part_num = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    part_cat_id = models.IntegerField()
    part_material = models.CharField(max_length=255)

class Set(models.Model):
    set_num = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    theme_id = models.IntegerField()
    num_parts = models.IntegerField()
    img_url = models.URLField()

class Theme(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent_id = models.IntegerField(null=True)
