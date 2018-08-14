from SWIFTDBApp import db

class Partners(db.Model):
    __tablename__ = 'partners'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(),nullable=False,unique=True)
    country = db.Column(db.String())
    role = db.Column(db.String())
    Deliverables_Rel = db.relationship('Deliverables')
    Tasks_Rel = db.relationship('Tasks')
    Users2Partners_Rel = db.relationship('Users2Partners')

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
    Users2Work_Packages_Rel = db.relationship('Users2Work_Packages')

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

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(),unique=True)
    password = db.Column(db.String())
    Users2Work_Packages_Rel = db.relationship('Users2Work_Packages')
    Users2Partners_Rel = db.relationship('Users2Partners')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Users2Work_Packages(db.Model):
    __tablename__ = 'users2work_packages'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(),db.ForeignKey('users.username'),nullable=False)
    work_package = db.Column(db.String(),db.ForeignKey('work_packages.code'),nullable=False)
    __table_args__ = (db.UniqueConstraint('username', 'work_package', name='_username_work_package_uc'),)

    def __init__(self, username, work_package):
        self.username = username
        self.work_package = work_package

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    code = db.Column(db.String(),nullable=False,unique=True)
    description = db.Column(db.String(),nullable=False)
    responsible_partner = db.Column(db.String(),db.ForeignKey('partners.name'),nullable=False)
    month_due = db.Column(db.Integer,nullable=False)
    progress = db.Column(db.String())
    percent = db.Column(db.Integer,nullable=False)

    def __init__(self, code, description, responsible_partner, month_due, progress, percent):
        self.code = code
        self.description = description
        self.responsible_partner = responsible_partner
        self.month_due = month_due
        self.progress = progress
        self.percent = percent

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Users2Partners(db.Model):
    __tablename__ = 'users2partners'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(),db.ForeignKey('users.username'),nullable=False)
    partner = db.Column(db.String(),db.ForeignKey('partners.name'),nullable=False)
    __table_args__ = (db.UniqueConstraint('username', 'partner', name='_username_partner_uc'),)

    def __init__(self, username, partner):
        self.username = username
        self.partner = partner

    def __repr__(self):
        return '<id {}>'.format(self.id)
