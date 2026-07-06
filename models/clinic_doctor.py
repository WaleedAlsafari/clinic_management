from odoo import models, fields, api


class ClinicDoctor(models.Model):
    _name = 'clinic.doctor'
    _description = 'Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    ref = fields.Char(default='New', readonly=True)
    name = fields.Char(related='partner_id.name', store=True, readonly=False, required=True)
    phone = fields.Char(related='partner_id.phone', store=True, readonly=False, required=True)
    email = fields.Char(related='partner_id.email', store=True, readonly=False,)
    partner_id = fields.Many2one('res.partner')
    user_id = fields.Many2one('res.users')
    specialization = fields.Char(required=True)
    license_no = fields.Char(string='License Number', required=True)
    active = fields.Boolean(default=True)
    appointment_ids = fields.One2many('clinic.appointment', 'doctor_id')
    appointment_count = fields.Integer(
        compute='_compute_appointment_ids'
    )


    _unique_name = models.Constraint('unique(name)', 'This name exist please use a different one')
    _unique_license_no = models.Constraint('unique(license_no)', 'Make sure to use a unique license number')
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
    'group_ids': [(6, 0, [
        self.env.ref('base.group_user').id,
        self.env.ref('clinic_management.clinic_doctor_group').id
    ])],

})      # ------- In order to use below function you must configure the mail server! --------- #
        # user.action_reset_password()

        rec.partner_id = partner.id
        rec.user_id = user.id
        rec.ref = self.env['ir.sequence'].next_by_code('clinic_doctor_seq')
        return rec
    
    def open_related_appointment_button(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Appointments',
        'res_model': 'clinic.appointment',
        'view_mode': 'list',
        'domain' : [('id','in', self.appointment_ids.ids)],
        'target': 'current',
        'context' : {
            'search_default_not_done':1
        }
     }
    
    @api.depends('appointment_ids')
    def _compute_appointment_ids(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids.filtered(lambda a: a.state != 'done'))


    

