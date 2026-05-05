from odoo import models, fields


class CreateFollowUp(models.TransientModel):
    _name='create.followup'

    appointment_id = fields.Many2one('clinic.appointment', readonly=1)
    appointment_date = fields.Date()
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
    
    parent_id = fields.Many2one('clinic.appointment')
    child_ids = fields.One2many('clinic.appointment', 'parent_id')


    def create_follow_up_appointment(self):
        rec = self.env['clinic.appointment'].create({
            'patient_id' : self.appointment_id.patient_id.id,
            'doctor_id' : self.appointment_id.doctor_id.id,
            'appointment_date' : self.appointment_date,
            'appointment_hour' : self.appointment_hour,
            'parent_id' : self.appointment_id.id,
            'is_follow_up' : True
        })
       
