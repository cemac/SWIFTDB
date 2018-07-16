from SWIFTDBApp import db

class Partners(db.Model):
    __tablename__ = 'partners'

    partner_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),unique=True, nullable=False)
    country = db.Column(db.String())
    role = db.Column(db.String())
    Deliverables_Rel = db.relationship('Deliverables')
    # Partners2Tasks_Rel = db.relationship('Partners2Tasks')

    def __init__(self, name, country, role):
        self.name = name
        self.country = country
        self.role = role

    def __repr__(self):
        return '<partner_id {}>'.format(self.partner_id)

class Work_Packages(db.Model):
    __tablename__ = 'work_packages'

    wp_id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    Deliverables_Rel = db.relationship('Deliverables')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<wp_id {}>'.format(self.wp_id)

class Deliverables(db.Model):
    __tablename__ = 'deliverables'

    deliverable_id = db.Column(db.String(), primary_key=True)
    work_package = db.Column(db.String(), db.ForeignKey('work_packages.wp_id'), nullable=False)
    description = db.Column(db.String(), nullable=False)
    responsible_partner = db.Column(db.Integer, db.ForeignKey('partners.partner_id'), nullable=False)
    month_due = db.Column(db.Integer)
    progress = db.Column(db.String())
    percent = db.Column(db.Integer, nullable=False)
    # Tasks2Deliverables_Rel = db.relationship('Tasks2Deliverables')
    # Partners2Tasks_Rel = db.relationship('Partners2Tasks')

    def __init__(self, work_package, description, responsible_partner, month_due, progress, percent):
        self.work_package = work_package
        self.description = description
        self.responsible_partner = responsible_partner
        self.month_due = month_due
        self.progress = progress
        self.percent = percent

    def __repr__(self):
        return '<deliverable_id {}>'.format(self.deliverable_id)

# class Tasks(db.Model):
#     __tablename__ = 'tasks'
#
#     task_id = db.Column(db.String(), primary_key=True)
#     description = db.Column(db.String(), nullable=False)
#     Tasks2Deliverables_Rel = db.relationship('Tasks2Deliverables')
#     Partners2Tasks_Rel = db.relationship('Partners2Tasks')
#
#     def __init__(self, description):
#         self.description = description
#
#     def __repr__(self):
#         return '<task_id {}>'.format(self.task_id)
#
# class Tasks2Deliverables(db.Model):
#     __tablename__ = 'tasks2deliverables'
#
#     t2d_id = db.Column(db.Integer, primary_key=True)
#     task = db.Column(db.String(), db.ForeignKey('tasks.task_id'), nullable=False)
#     deliverable = db.Column(db.String(), db.ForeignKey('deliverbles.deliverable_id'), nullable=False)
#
#     def __init__(self, task, deliverable):
#         self.task = task
#         self.deliverable = deliverable
#
#     def __repr__(self):
#         return '<t2d_id {}>'.format(self.t2d_id)
#
# class Partners2Tasks(db.Model):
#     __tablename__ = 'partners2tasks'
#
#     p2td_id = db.Column(db.Integer, primary_key=True)
#     partner = db.Column(db.Integer, db.ForeignKey('partners.partner_id'))
#     task_or_deliverable = db.Column(db.Boolean)
#     task = db.Column(db.String(),db.ForeignKey('tasks.task_id'))
#     deliverable = db.Column(db.String(),db.ForeignKey('deliverbles.deliverable_id'))
#     progress = db.Column(db.String())
#     percent = db.Column(db.Integer)
#
#     def __init__(self, partner, task_or_deliverable, task, deliverable, progress, percent):
#         self.partner = partner
#         self.task_or_deliverable = task_or_deliverable
#         self.task = task
#         self.deliverable = deliverable
#         self.progress = progress
#         self.percent = percent
#
#     def __repr__(self):
#         return '<p2td_id {}>'.format(self.p2td_id)
