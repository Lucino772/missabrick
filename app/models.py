from app import db

class Color(db.Model):
    __tablename__ = 'colors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    rgb = db.Column(db.String(6), nullable=False)
    is_trans = db.Column(db.String(10), nullable=False)

class Element(db.Model):
    __tablename__ = 'elements'

    element_id = db.Column(db.String(10), primary_key=True)
    
    part_num = db.Column(db.String(20), db.ForeignKey('parts.part_num'), nullable=False)
    part = db.relationship('Part', backref=db.backref('elements', lazy=True))
    
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)
    color = db.relationship('Color', backref=db.backref('elements', lazy=True))

class Inventory(db.Model):
    __tablename__ = 'inventories'

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, nullable=False)
    
    set_num = db.Column(db.String(20), db.ForeignKey('sets.set_num'), nullable=False)
    _set = db.relationship('Set', backref=db.backref('inventories', lazy=True))

class InventoryMinifigs(db.Model):
    __tablename__ = 'inventory_minifigs'

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventories.id'))
    fig_num = db.Column(db.String(20), db.ForeignKey('minifigs.fig_num'))
    quantity = db.Column(db.Integer)

class InventoryParts(db.Model):
    __tablename__ = 'inventory_parts'

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventories.id'))
    part_num = db.Column(db.String(20), db.ForeignKey('parts.part_num'))
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'))
    quantity = db.Column(db.Integer)
    is_spare = db.Column(db.String(10), nullable=False)

class InventorySets(db.Model):
    __tablename__ = 'inventory_sets'

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventories.id'))
    set_num = db.Column(db.String(20), db.ForeignKey('sets.set_num'))
    quantity = db.Column(db.Integer)

class Minifig(db.Model):
    __tablename__ = 'minifigs'

    fig_num = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    num_parts = db.Column(db.Integer, nullable=False)

class PartCategory(db.Model):
    __tablename__ = 'part_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

class PartRelationship(db.Model):
    __tablename__ = 'part_relationships'

    rel_type = db.Column(db.String(1), primary_key=True)
    child_part_num = db.Column(db.String(20), db.ForeignKey('parts.part_num'), primary_key=True)
    parent_part_num = db.Column(db.String(20), db.ForeignKey('parts.part_num'), primary_key=True)

class Part(db.Model):
    __tablename__ = 'parts'

    part_num = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    part_cat_id = db.Column(db.Integer, db.ForeignKey('part_categories.id'), nullable=False)
    part_cat = db.relationship('PartCategory', backref=db.backref('parts', lazy=True))

    part_material = db.Column(db.String(200))

class Set(db.Model):
    __tablename__ = 'sets'

    set_num = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=False)
    theme = db.relationship('Theme', backref=db.backref('sets', lazy=False))

    num_parts = db.Column(db.Integer, nullable=False)

class Theme(db.Model):
    __tablename__ = 'themes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=True)
