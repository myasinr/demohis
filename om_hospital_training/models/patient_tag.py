# -*- coding: utf-8 -*-
from odoo import fields, models


class HospitalPatientTag(models.Model):
    _name = 'hospital.patient.tag'
    _description = 'Patient Tag / Disease / Skill'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('hospital_patient_tag_name_unique', 'unique(name)', 'Tag name must be unique.'),
    ]
