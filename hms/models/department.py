from odoo import fields, models


class Department(models.Model):
    _rec_name = "department_name"
    _name = 'hms.department'

    department_name = fields.Char()
    is_opened = fields.Boolean()
    capacity = fields.Integer()

    patient_ids = fields.One2many("hms.patient", "department_id")
