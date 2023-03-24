from odoo import models, fields,api 
from datetime import datetime
from odoo.exceptions import ValidationError
class Patient(models.Model):
    _name = 'hms.patient'

    firstname=fields.Char(string='First Name')
    lastname=fields.Char(string='Last Name')
    birhtdate=fields.Date(string='Birth Date')
    CR_Ratio=fields.Float(string='CR Ratio')
    blood_type=fields.Selection(string='Blood Type', selection=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'),('O-','O-')])
    Pcr=fields.Boolean(string='PCR')
    images=fields.Image(string='Images')
    address=fields.Text(string='Address')
    age=fields.Integer(string='Age')
    state = fields.Selection([
    ('undetermined', 'Undetermined'),
    ('good', 'Good'),
    ('fair', 'Fair'),
    ('serious', 'Serious')
], string='State', default='undetermined')
    departemnt_id=fields.Many2one('hms.department', string='Department')
    doctors_id=fields.Many2many('hms.doctors', string='Doctors')
    history=fields.Char(string='History')
    email=fields.Char(string='Email')
    computed_age=fields.Integer(compute='compute_age')
    logs_id=fields.One2many('hms.patientlog', 'patient_id', string='Logs')
    _sql_constraints = [ ('unique_name','UNIQUE(email)','Email Already Exists') ]
    related_lead_id = fields.Many2one('res.partner', string='Related Lead', inverse_name='related_patient_id')

    # to make the column age changes directly when the birhtdate changes
    @api.depends('birhtdate')
    def compute_age(self):
        for record in self:
            if record.birhtdate:
                record.computed_age=datetime.now().year-record.birhtdate.year
                record.age=record.computed_age
               
            else:
                record.computed_age=0

    @api.onchange('birhtdate')
    def on_change_birhtdate(self):
        if self.birhtdate:
            self.age=datetime.now().year-self.birhtdate.year
            if self.age < 30:
                    self.Pcr=True
                    return { 
                        'warning': {
                        'title':'Pcr checked',
                        'message':'Pcr was automatically checked'
                    }}
            # to make an alert for the user that the age is changed
     
    def set_to_serious(self):
        self.state = 'serious'

    def set_to_good(self):
        self.state = 'good'
    def set_to_fair(self):
        self.state = 'fair'
#####################################################################################################################
    def write(self, vals):
            if 'state' in vals:
                description=f"State changed from {self.state} to {vals['state']}"
                logValues={
                'description':description,
                'patient_id':self.id,
                }
                self.env['hms.patientlog'].create(logValues)
                return super(Patient, self).write(vals)
############################################################################################################################



    @api.constrains('email')
    def check_email(self):
        for record in self:
            if '@' not in record.email:
                raise ValidationError('Please enter a valid email address')

    # @api.model
    # def create(self,vals):
    #     if '@' not in vals['email']:
    #         vals['email'] = vals['email']+'@gmail.com'
    #     return super().create(vals)






# steps for lab
# 1. install crm module 
# 2.create a new crm module
# 3. put inside it the init file + manifest file ---> contains name and depends and inside depends put the name of the module in the odoo website that you want to edit
# 4.create models folder and create init file inside it and a python file to write our class inside it
# 5. the class is in the screenshots
# 6. create views folder and inside it create the xml and put it inside the manifest
# 7. edit view from the debug icon and then get the external id and this id will be used in the views xml 
# 8. add <field name='inherit_id' ref='externalid'/>
# 9. decide where you want to put your field  and wrap your new field inside it as in screenshots 
# 10. upgrade your apps

#11.create_uid#
# 
# #