from SWIFTDBApp import db

class Partners(db.Model):
    __tablename__ = 'partners'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(),nullable=False,unique=True)
    country = db.Column(db.String())
    role = db.Column(db.String())
    Deliverables_Rel = db.relationship('Deliverables')

    def __init__(self, name, country, role):
        self.name = name
        self.country = country
        self.role = role

    def __repr__(self):
        return '<name {}>'.format(self.name)

class Work_Packages(db.Model):
    __tablename__ = 'work_packages'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    code = db.Column(db.String(),nullable=False,unique=True)
    name = db.Column(db.String(),nullable=False)
    Deliverables_Rel = db.relationship('Deliverables')

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Deliverables(db.Model):
    __tablename__ = 'deliverables'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    code = db.Column(db.String(),nullable=False,unique=True)
    work_package = db.Column(db.String(),db.ForeignKey('work_packages.code'),nullable=False)
    description = db.Column(db.String(),nullable=False)
    responsible_partner = db.Column(db.String(),db.ForeignKey('partners.name'),nullable=False)
    month_due = db.Column(db.Integer,nullable=False)
    progress = db.Column(db.String())
    percent = db.Column(db.Integer,nullable=False)

    def __init__(self, code, work_package, description, responsible_partner, month_due, progress, percent):
        self.code = code
        self.work_package = work_package
        self.description = description
        self.responsible_partner = responsible_partner
        self.month_due = month_due
        self.progress = progress
        self.percent = percent

    def __repr__(self):
        return '<id {}>'.format(self.id)
