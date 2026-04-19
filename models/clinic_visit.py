from odoo import models, fields, api


class ClinicVisit(models.Model):
    _name = 'clinic.visit'
    _description = 'Visit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    visit_no = fields.Char(readonly=1)
    appointment_id = fields.Many2one('clinic.appointment')
    appointment_date = fields.Date(related='appointment_id')
    appointment_hour = fields.Selection(related='appointment_id')
    patient_id = fields.Many2one('clinic.patient')
    doctor_id = fields.Many2one('clinic.doctor')
    complaint = fields.Text()
    diagnosis = fields.Text()
    note = fields.Text()
    state = fields.Selection([
        ('draft','Draft'),
        ('in_consultation','In Consultation'),
        ('done','Done'),
        ('invoiced', 'Invoiced'),
        ('cancelled','Cancelled'),
    ])

