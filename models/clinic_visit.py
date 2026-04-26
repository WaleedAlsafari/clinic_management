from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ClinicVisit(models.Model):
    _name = 'clinic.visit'
    _description = 'Visit'
    _rec_name = 'visit_no'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    visit_no = fields.Char(default='New',readonly=1, string='Visit Number')
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment Reference', readonly=1)
    visit_date = fields.Date(related='appointment_id.appointment_date', string='Visit Date', store=1)
    visit_hour = fields.Selection(related='appointment_id.appointment_hour', string='Visit Time', store=1, readonly=0)
    patient_id = fields.Many2one(related='appointment_id.patient_id', store=1, readonly=1)
    doctor_id = fields.Many2one(related='appointment_id.doctor_id', store=1, readonly=1)
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
    prescription_line_ids = fields.One2many('clinic.prescription.line', 'visit_id')
    invoice_id = fields.Many2one('account.move')
    service_line_ids = fields.One2many(comodel_name='clinic.service.line', string='Service', inverse_name='visit_id', required=1)

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
            if not rec.complaint:
                raise ValidationError("Complaint must be filled")
            if not rec.diagnosis:
                raise ValidationError("Diagnosis must be filled")
                

    def mark_as_invoiced(self):
        for rec in self:
            rec.state='invoiced'
            rec.create_invoice()

    def mark_as_cancelled(self):
        for rec in self:
            rec.state='cancelled'

    def create_invoice(self):
        self.ensure_one()

        lines = []

        for line in self.prescription_line_ids:
            lines.append((0,0,{
                'product_id' : line.product_id.id,
                'name' : line.product_id.name,
                'quantity' : line.quantity,
                'price_unit' : line.product_id.list_price
            }))
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id' : self.patient_id.partner_id.id,
            'invoice_date' : fields.Date.today(),
            'invoice_line_ids' : lines
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current'
    }



    @api._model_create_multi
    def create(self,vals):
        rec = super(ClinicVisit,self).create(vals)
        rec.mark_as_draft()
        return rec


    @api.constrains('service_line_ids')
    def check_service_line_exist(self):
        for rec in self:
            if not rec.service_line_ids:
                raise ValidationError("Error: at least one service must be selected")
    

class ClinicPrescriptionLine(models.Model):
    _name='clinic.prescription.line'

    visit_id = fields.Many2one('clinic.visit')
    product_id = fields.Many2one('product.product')
    quantity  = fields.Integer(required=1, default=1)
    dosage = fields.Char()
    frequency = fields.Char()
    duration = fields.Char()
    instructions = fields.Text()

class ClinicServiceLine(models.Model):
    _name='clinic.service.line'

    visit_id = fields.Many2one('clinic.visit')
    product_id = fields.Many2one('product.product', string='Service')
    quantity = fields.Integer(required=1, default=1)
    
    




