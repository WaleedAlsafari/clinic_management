from odoo import models, fields, api



class ClinicAppointment(models.Model):
    _name = 'clinic.appointment'

    appointment_no = fields.Char(default="New", readonly=1, string='Appointment Number')
    patient_id = fields.Many2one('clinic.patient', required=1)
    doctor_id = fields.Many2one('clinic.doctor', required=1)
    appointment_date = fields.Date(requried=1)
    appointment_date = fields.Datetime(requried=1)
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



