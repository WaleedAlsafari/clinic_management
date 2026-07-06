import pytz

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import time, datetime, timedelta


class ClinicAppointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'
    _rec_name = 'appointment_no'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    appointment_no = fields.Char(default="New", readonly=True, string='Appointment Number')
    patient_id = fields.Many2one('clinic.patient', required=True)
    doctor_id = fields.Many2one('clinic.doctor', required=True)
    appointment_date = fields.Date(required=True)
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
], string='Appointment Time', required=True)
    calendar_start = fields.Datetime(compute='compute_calendar', string="Start", store=True)
    calendar_end = fields.Datetime(compute='compute_calendar', string="End", store=True)
    reason = fields.Text()
    state = fields.Selection([
        ('draft','Draft'),
        ('confirmed',"Confirmed"),
        ('in_progress','In Progress'),
        ('done','Done'),
        ('cancelled','Cancelled')
    ],
    group_expand='_expand_states'
    )
    notes = fields.Text()
    visit_id = fields.Many2one('clinic.visit')
    invoice_id = fields.Many2one('account.move')
    is_follow_up = fields.Boolean(default=False, readonly=True)
    parent_id = fields.Many2one('clinic.appointment')
    child_ids = fields.One2many('clinic.appointment', 'parent_id')
    
    @api.constrains('appointment_date', 'appointment_hour')
    def _check_available_time_slot(self):
        for rec in self:
            match = rec.search([('appointment_date','=',rec.appointment_date), ('appointment_hour','=', rec.appointment_hour), ('doctor_id', '=', rec.doctor_id.id), ('id' , '!=', rec.id)])
            if match:
                raise ValidationError("This time slot is booked, please use a different one")
            
    @api.model_create_multi
    def create(self,vals):
        rec = super(ClinicAppointment,self).create(vals)
        rec.mark_as_draft()
        return rec
    
    # @api.model
    # def search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     records = super(ClinicAppointment,self).search(domain, offset=0, limit=None, order=None)
    #     print("within serarch method")
    #     for rec in records:
    #         print(rec.doctor_id.user_id)
    #         print(self.env.user.id)
    #     return records

    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancelled'):
                raise ValidationError("You can't delete this appointment unless it's draft or cancelled")
        return super().unlink()

    def mark_as_draft(self):
        for rec in self:
            rec.state = 'draft'

    def mark_as_confirmed(self):
        for rec in self:
            rec.state = 'confirmed'
            rec.appointment_no = self.env['ir.sequence'].next_by_code('clinic_appointment_seq')

    def mark_as_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'
            rec.visit_id = self.env['clinic.visit'].sudo().create({"appointment_id" : rec.id})

    def mark_as_done(self):
        for rec in self:
            rec.state = 'done'

    def mark_as_cancelled(self):
        for rec in self:
            rec.state = 'cancelled'

    @api.constrains('appointment_date')
    def _validate_selected_appointment_date(self):
        for rec in self:
            if rec.appointment_date < fields.Date.today():
                raise ValidationError("Invalid appointment date")

    @api.constrains('appointment_hour')
    def _validate_selected_appointment_time(self):
        
        now_time = fields.Datetime.context_timestamp(self, fields.Datetime.now()).time()
        for rec in self:
            if rec.appointment_date == fields.Date.today():
                h, m = rec.appointment_hour.split(':')
                rec_time = time(int(h), int(m))
                if rec_time < now_time:
                    raise ValidationError("Invalid appointment time")

    def show_create_follow_up_appointment(self):
        if self.state == 'done':
            action = self.env['ir.actions.actions']._for_xml_id('clinic_management.action_create_follow_up_wizard')
            action['context'] = {'default_appointment_id' : self.id}
            return action
        else:
            raise ValidationError("Error, can't create follow up appointment if it's not done")
    @api.depends('appointment_date', 'appointment_hour')
    def compute_calendar(self):
        tz = pytz.timezone('Asia/Riyadh')

        for rec in self:
            if rec.appointment_date and rec.appointment_hour:

                dt_str = f"{rec.appointment_date} {rec.appointment_hour}"

                local_dt = fields.Datetime.to_datetime(dt_str)

                local_dt = tz.localize(local_dt)

                utc_dt = local_dt.astimezone(pytz.utc).replace(tzinfo=None)

                rec.calendar_start = utc_dt
                rec.calendar_end = utc_dt + timedelta(minutes=30)
    
    @api.model
    def _expand_states(self, states, domain):
        return [key for key, val in type(self).state.selection]
    def open_related_visit_button(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visit',
            'res_model': 'clinic.visit',
            'view_mode': 'form',
            'res_id': self.visit_id.id,
            'target': 'current'   
        }   

    






