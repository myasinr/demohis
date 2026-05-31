# -*- coding: utf-8 -*-
from odoo import fields, models


class HospitalPatientTag(models.Model):
    _name = 'hospital.patient.tag'
    _description = 'Patient Tag / Disease'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(default=True)
