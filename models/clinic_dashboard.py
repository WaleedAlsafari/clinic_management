from odoo import models, fields, api
from datetime import timedelta


class ClinicDashboard(models.Model):
    _name = 'clinic.dashboard'
    _description = 'Clinic Dashboard'

    @api.model
    def get_dashboard_data(self):
        today = fields.Date.context_today(self)
        week_start = today - timedelta(days=6)

        return {
            'kpi': self._get_kpis(today),
            'appointment_states': self._get_appointment_state_breakdown(),
            'week_trend': self._get_week_trend(week_start, today),
            'today_appointments': self._get_today_appointments(today),
            'recent_patients': self._get_recent_patients(),
        }

    def _get_kpis(self, today):
        Patient = self.env['clinic.patient']
        Doctor = self.env['clinic.doctor']
        Appointment = self.env['clinic.appointment']
        Visit = self.env['clinic.visit']

        return {
            'total_patients': Patient.search_count([]),
            'total_doctors': Doctor.search_count([('active', '=', True)]),
            'today_appointments': Appointment.search_count(
                [('appointment_date', '=', today)]
            ),
            'upcoming_appointments': Appointment.search_count([
                ('appointment_date', '>', today),
                ('state', 'in', ['draft', 'confirmed']),
            ]),
            'visits_in_progress': Visit.search_count(
                [('state', '=', 'in_consultation')]
            ),
            'completed_visits_today': Visit.search_count([
                ('visit_date', '=', today),
                ('state', 'in', ['done', 'invoiced']),
            ]),
        }

    def _get_appointment_state_breakdown(self):
        Appointment = self.env['clinic.appointment']
        states = [key for key, _ in Appointment._fields['state'].selection]
        groups = Appointment.read_group([], ['state'], ['state'])
        counts = {g['state']: g['state_count'] for g in groups}
        labels = dict(Appointment._fields['state'].selection)
        return [
            {'state': s, 'label': labels[s], 'count': counts.get(s, 0)}
            for s in states
        ]

    def _get_week_trend(self, start_date, today):
        Appointment = self.env['clinic.appointment']
        data = []
        for i in range(7):
            d = start_date + timedelta(days=i)
            count = Appointment.search_count([('appointment_date', '=', d)])
            data.append({
                'date': d.strftime('%Y-%m-%d'),
                'label': d.strftime('%a'),
                'count': count,
            })
        return data

    def _get_today_appointments(self, today):
        appointments = self.env['clinic.appointment'].search([
            ('appointment_date', '=', today),
        ], order='appointment_hour', limit=8)

        return [{
            'id': a.id,
            'patient': a.patient_id.name or '',
            'doctor': a.doctor_id.name or '',
            'time': a.appointment_hour or '',
            'state': a.state,
        } for a in appointments]

    def _get_recent_patients(self):
        patients = self.env['clinic.patient'].search(
            [], order='id desc', limit=5
        )
        return [{
            'id': p.id,
            'name': p.name or '',
            'ref': p.ref or '',
        } for p in patients]