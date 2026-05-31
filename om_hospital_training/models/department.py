# -*- coding: utf-8 -*-
from odoo import fields, models


class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'
    _order = 'sequence, name'

    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    code = fields.Char(required=True)
    active = fields.Boolean(default=True)
    note = fields.Text()

    _sql_constraints = [
        ('hospital_department_code_unique', 'unique(code)', 'Department code must be unique.'),
        ('hospital_department_name_unique', 'unique(name)', 'Department name must be unique.'),
    ]
