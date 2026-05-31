# -*- coding: utf-8 -*-
from odoo import fields, models


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(readonly=True, copy=False, default='New', tracking=True)
    department_id = fields.Many2one('hospital.department', required=True, ondelete='restrict', tracking=True)
    specialization = fields.Selection([
        ('general', 'General Physician'),
        ('cardiology', 'Cardiology'),
        ('pediatrics', 'Pediatrics'),
        ('orthopedic', 'Orthopedic'),
        ('neurology', 'Neurology'),
    ], default='general', tracking=True)
    mobile = fields.Char()
    email = fields.Char()
    active = fields.Boolean(default=True)
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id')
    appointment_count = fields.Integer(compute='_compute_appointment_count')

    def _compute_appointment_count(self):
        data = self.env['hospital.appointment'].read_group(
            [('doctor_id', 'in', self.ids)], ['doctor_id'], ['doctor_id']
        )
        mapped = {row['doctor_id'][0]: row['doctor_id_count'] for row in data if row.get('doctor_id')}
        for rec in self:
            rec.appointment_count = mapped.get(rec.id, 0)

    def name_get(self):
        result = []
        for rec in self:
            name = '[%s] %s' % (rec.code or 'New', rec.name or '')
            result.append((rec.id, name))
        return result

    def action_view_appointments(self):
        self.ensure_one()
        action = self.env.ref('om_hospital_training.action_hospital_appointment').read()[0]
        action['domain'] = [('doctor_id', '=', self.id)]
        action['context'] = {'default_doctor_id': self.id}
        return action

    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or 'New'
        return super(HospitalDoctor, self).create(vals)
