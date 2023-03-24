from odoo import models, fields,api
from odoo.exceptions import ValidationError


class CrmPatient(models.Model):
    _inherit="res.partner"

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')
    vat=fields.Char(required=True)


    
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                checking=self.env['hms.patient'].search([('email', '=', record.email)])
                if checking:
                    raise ValidationError(('This email is already registered'))

    
    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError(('You cannot delete this record'))
        return super(CrmPatient, self).unlink()