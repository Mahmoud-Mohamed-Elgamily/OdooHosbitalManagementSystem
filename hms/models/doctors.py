from odoo import models, fields


class Doctor(models.Model):
    _rec_name = "first_name"
    _name = "hms.doctor"

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Binary()

    department_id = fields.Many2one("hms.department")
