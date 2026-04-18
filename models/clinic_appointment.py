from odoo import models, fields, api
from odoo.exceptions import ValidationError



class ClinicAppointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'
    _rec_name = 'appointment_no'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    appointment_no = fields.Char(default="New", readonly=1, string='Appointment Number')
    patient_id = fields.Many2one('clinic.patient', required=1)
    doctor_id = fields.Many2one('clinic.doctor', required=1)
    appointment_date = fields.Date(required=1)
    appointment_hour = fields.Selection([
    ('09:00', '09:00'),
    ('09:30', '09:30'),
    ('10:00', '10:00'),
    ('10:30', '10:30'),
    ('11:00', '11:00'),
    ('11:30', '11:30'),
    ('12:00', '12:00'),
    ('12:30', '12:30'),
    ('13:00', '13:00'),
    ('13:30', '13:30'),
    ('14:00', '14:00'),
    ('14:30', '14:30'),
    ('15:00', '15:00'),
    ('15:30', '15:30'),
    ('16:00', '16:00'),
    ('16:30', '16:30'),
], string='Appointment Time', required=1)
    reason = fields.Text()
    state = fields.Selection([
        ('draft','Draft'),
        ('confirmed',"Confirmed"),
        ('in_progress','In Progress'),
        ('done','Done'),
        ('cancelled','Cancelled')
    ]
    )
    notes = fields.Text()
    # visit_id = fields.Many2one('clinic.visit')
    invoice_id = fields.Many2one('account.move')

    @api.constrains('appointment_date', 'appointment_hour')
    def _check_available_time_slot(self):
        for rec in self:
            match = rec.search([('appointment_date','=',rec.appointment_date), ('appointment_hour','=', rec.appointment_hour), ('doctor_id', '=', rec.doctor_id.id), ('id' , '!=', rec.id)])
            if match:
                raise ValidationError("This time slot is booked, please use a different one")
            
    @api.model_create_multi
    def create(self,vals):
        rec = super(ClinicAppointment,self).create(vals)
        rec.appointment_no = self.env['ir.sequence'].next_by_code('clinic_appointment_seq')
        return rec






