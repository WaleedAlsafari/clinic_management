from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ClinicVisit(models.Model):
    _name = 'clinic.visit'
    _description = 'Visit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    visit_no = fields.Char(default='New',readonly=1)
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment Reference', readonly=1)
    visit_date = fields.Date(related='appointment_id.appointment_date', string='Visit Date', store=1)
    visit_hour = fields.Selection(related='appointment_id.appointment_hour', string='Visit Time', store=1, readonly=0)
    patient_id = fields.Many2one(related='appointment_id.patient_id', store=1)
    doctor_id = fields.Many2one(related='appointment_id.doctor_id', store=1)
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
    # prescription_line_ids = fields.One2many(comodel_name=)
    # invoice_id = fields.Many2one()
    # service_product_id = fields.Many2one()
    # amount_total = fields.Monetary(currency_field=)

    def mark_as_draft(self):
        for rec in self:
            rec.state='draft'

    def mark_as_in_consultation(self):
        for rec in self:
            rec.state='in_consultation'
            rec.visit_no = self.env['ir.sequence'].next_by_code('clinic_visit_seq')

    def mark_as_done(self):
        for rec in self:
            rec.state='done'
            if rec.appointment_id:
                rec.appointment_id.write({'state' : rec.state})
            else:
                raise ValidationError("Error, no appointment is linked!")

    def mark_as_invoiced(self):
        for rec in self:
            rec.state='invoiced'

    def mark_as_cancelled(self):
        for rec in self:
            rec.state='cancelled'

    @api._model_create_multi
    def create(self,vals):
        rec = super(ClinicVisit,self).create(vals)
        rec.mark_as_draft()
        return rec


