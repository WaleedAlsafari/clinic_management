from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ClinicPatient(models.Model):
    _name = 'clinic.patient'
    _description = 'Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
<<<<<<< HEAD
=======
    
>>>>>>> dev

    ref = fields.Char(default='New', readonly=True)
    partner_id = fields.Many2one('res.partner')
    name = fields.Char(related = 'partner_id.name', string='Name', store=True, requried=True, readonly=False)
    phone = fields.Char(related = 'partner_id.phone', string='Phone', store=True, requried=True, readonly=False, size=10)
    nid = fields.Char(requried=True, string='National Id', size=10)
    age = fields.Integer(requried=True)
    weight = fields.Float()
    hight = fields.Float()
    date_of_birth = fields.Date(required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female','Female'),
    ], required=True )
    blood_type = fields.Selection([
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
    ], required=True )
    insurance_no = fields.Char(required=True, string='Insurance Number')
    emergency_contact = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name','unique(name)','This patient name exist, please use different one'),
        ('unique_nid','unique(nid)','This patient id exist, please use different one'),
    ]


    @api.model_create_multi
    def create(self,vals):
        rec = super(ClinicPatient,self).create(vals)
        rec._check_age_not_zero()
        partner =  self.env['res.partner'].create({'name' : rec.name, 'phone' : rec.phone })
        print(partner.id)
        rec.partner_id = partner.id
        rec.ref = self.env['ir.sequence'].next_by_code('clinic_patient_seq')
        return rec

    def _check_age_not_zero(self):
        for rec in self:
            if rec.age <= 0:
                raise ValidationError("Please enter a valid age")
    
