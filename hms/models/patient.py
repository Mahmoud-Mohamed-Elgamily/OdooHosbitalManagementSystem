from odoo import models, fields, api
from datetime import datetime, date
import re
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _rec_name = "first_name"
    _name = "hms.patient"

    department_capacity = fields.Integer(related="department_id.capacity")
    blood_type = fields.Selection([('a', 'a'), ('b', 'b'), ('o', 'o')])
    first_name = fields.Char()
    birth_date = fields.Date()
    last_name = fields.Char()
    cr_ratio = fields.Float()
    address = fields.Char()
    history = fields.Html()
    image = fields.Binary()
    email = fields.Char()
    pcr = fields.Boolean()
    age = fields.Integer()
    state = fields.Selection([
        ('Undetermined', 'Undetermined'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Serious', 'Serious'),
    ], default="Undetermined")

    department_id = fields.Many2one("hms.department")
    customer_ids = fields.One2many("res.partner", "related_patient_id")
    doctor_id = fields.Many2many("hms.doctor")
    log_ids = fields.One2many("hms.patient_log", "patient_id")

    def change_state(self):
        if self.state == "Undetermined":
            self.state = "Good"
        elif self.state == "Good":
            self.state = "Fair"
        elif self.state == "Fair":
            self.state = "Serious"

        self.log_ids.create({"updates": f"State changed to {self.state}", "patient_id": self.id})

    @api.onchange('age')
    def change_age(self):
        if self.age:
            if self.age < 30:
                self.pcr = True
                return {"warning": {"title": "PCR", "message": "the pcr is now checked"}}

    @api.constrains('email')
    def validate_mail(self):
        if self.email:
            if not re.match('^[_a-z0-9-]+(\\.[_a-z0-9-]+)*@[a-z0-9-]+(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$', self.email):
                raise ValidationError('Not a valid E-mail ID')

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for patient in self:
            self.age = today.year - patient.birth_date.year - ((today.month, today.day) < (patient.birth_date.month, patient.birth_date.day))

    _sql_constraints = [
        ('unique_email', 'UNIQUE (email)', 'You can not have two users with the same name !')
    ]


class PatientLog(models.Model):
    _name = "hms.patient_log"

    updates = fields.Text()
    time = fields.Datetime(default=datetime.today())

    current_user = fields.Many2one('res.users', 'by User', default=lambda self: self.env.user.id, readonly=True)
    patient_id = fields.Many2one("hms.patient")

    @api.model
    def create(self, values):
        new_record = super().create(values)
        return new_record
