from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from .patient import Patient


class PatientCustomer(models.Model):
    _inherit = "res.partner"
    related_patient_id = fields.Many2one("hms.patient")
    email = fields.Char()  # related="related_patient_id.email")
    vat = fields.Char(required=True)

    @api.multi
    def unlink(self):
        if self.related_patient_id:
            raise ValidationError('this customer is linked with a patient')
        else:
            super().unlink()


    @api.constrains('email')
    def check_mail(self):
        if self.email:
            if re.match('^[_a-z0-9-]+(\\.[_a-z0-9-]+)*@[a-z0-9-]+(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$', self.email):
                if self.related_patient_id.search([('email', '=', self.email)]):
                    raise ValidationError("email is the same as patient email")
            else:
                raise ValidationError("Wrong Email Format")
