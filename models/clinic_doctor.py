from odoo import models, fields, api


class ClinicDoctor(models.Model):
    _name = 'clinic.doctor'
    _description = 'Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    ref = fields.Char(default='New', readonly=True)
    name = fields.Char(related='partner_id.name', store=True, readonly=False, requried=1)
    phone = fields.Char(related='partner_id.phone', store=True, readonly=False, requried=1)
    email = fields.Char(related='partner_id.email', store=True, readonly=False,)
    partner_id = fields.Many2one('res.partner')
    user_id = fields.Many2one('res.user')
    specialization = fields.Char(requried=1)
    license_no = fields.Char(string='License Number', requried=1)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'This name exist please use a different one'),
        ('unique_license_no', 'unique(license_no)', 'Make sure to use a unique license number')
    ]
    @api.model_create_multi
    def create(self,vals):
        rec = super(ClinicDoctor,self).create(vals)
        partner = self.env['res.partner'].create({'name' : rec.name, 'phone' : rec.phone, 'email' : rec.email})
        user = self.env['res.users'].create({
    'name': rec.name,
    'login': rec.email,
    'email': rec.email,
    'password': 'Temp123@',
    'partner_id': partner.id,
    'groups_id': [(6, 0, [
        self.env.ref('base.group_user').id,
        self.env.ref('clinic_management.clinic_doctor_group').id
    ])],

})      # ------- In order to use below function you must configure the mail server! --------- #
        # user.action_reset_password()

        rec.partner_id = partner.id
        rec.user_id = user.id
        rec.ref = self.env['ir.sequence'].next_by_code('clinic_doctor_seq')
        return rec

    

