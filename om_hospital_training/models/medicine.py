# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalMedicine(models.Model):
    _name = 'hospital.medicine'
    _description = 'Hospital Medicine'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    price = fields.Float(default=0.0)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('hospital_medicine_code_unique', 'unique(code)', 'Medicine code must be unique.'),
        ('hospital_medicine_price_check', 'CHECK(price >= 0)', 'Medicine price cannot be negative.'),
    ]

    @api.constrains('price')
    def _check_price(self):
        for rec in self:
            if rec.price < 0:
                raise ValidationError('Medicine price cannot be negative.')
