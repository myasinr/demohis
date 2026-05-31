# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'
    _order = 'name'

    code = fields.Char(default='New', readonly=True, copy=False, tracking=True)
    name = fields.Char(required=True, tracking=True)
    display_name = fields.Char(compute='_compute_display_name', store=True)
    department_id = fields.Many2one('hospital.department', required=True, ondelete='restrict', tracking=True)
    specialization = fields.Char(tracking=True)
    mobile = fields.Char()
    email = fields.Char()
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id')
    appointment_count = fields.Integer(compute='_compute_appointment_count')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)

    _sql_constraints = [
        ('hospital_doctor_code_unique', 'unique(code)', 'Doctor code must be unique.'),
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or 'New'
        return super(HospitalDoctor, self).create(vals)

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = '[%s] %s' % (rec.code or 'New', rec.name or '')

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        grouped = self.env['hospital.appointment'].read_group(
            [('doctor_id', 'in', self.ids)], ['doctor_id'], ['doctor_id']
        )
        counts = {row['doctor_id'][0]: row['doctor_id_count'] for row in grouped if row.get('doctor_id')}
        for rec in self:
            rec.appointment_count = counts.get(rec.id, 0)

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email and '@' not in rec.email:
                raise ValidationError(_('Please enter a valid email address.'))

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '[%s] %s' % (rec.code or 'New', rec.name or '')))
        return result

    def action_view_appointments(self):
        self.ensure_one()
        action = self.env.ref('om_hospital_training.action_hospital_appointment').read()[0]
        action['domain'] = [('doctor_id', '=', self.id)]
        action['context'] = {'default_doctor_id': self.id}
        return action
