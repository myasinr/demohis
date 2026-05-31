# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'sequence, name'

    sequence = fields.Integer(default=10)
    name = fields.Char(required=True, tracking=True)
    code = fields.Char(required=True, tracking=True)
    active = fields.Boolean(default=True)
    doctor_ids = fields.One2many('hospital.doctor', 'department_id', string='Doctors')
    doctor_count = fields.Integer(compute='_compute_doctor_count')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)

    _sql_constraints = [
        ('hospital_department_code_unique', 'unique(code)', 'Department code must be unique.'),
    ]

    @api.depends('doctor_ids')
    def _compute_doctor_count(self):
        grouped = self.env['hospital.doctor'].read_group(
            [('department_id', 'in', self.ids)], ['department_id'], ['department_id']
        )
        counts = {row['department_id'][0]: row['department_id_count'] for row in grouped if row.get('department_id')}
        for rec in self:
            rec.doctor_count = counts.get(rec.id, 0)
