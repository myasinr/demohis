# -*- coding: utf-8 -*-
from odoo import fields, models


class HospitalVipPatient(models.Model):
    """Classical inheritance demo: new model reusing hospital.patient structure.

    In Odoo 13, inherited Many2many fields need their own relation table when _name + _inherit
    creates a new model/table. Therefore tag_ids is redefined here.
    """
    _name = 'hospital.vip.patient'
    _inherit = 'hospital.patient'
    _description = 'VIP Patient Demo Model'

    tag_ids = fields.Many2many(
        'hospital.patient.tag',
        'hospital_vip_patient_tag_rel',
        'vip_patient_id',
        'tag_id',
        string='Tags / Diseases'
    )
    vip_level = fields.Selection([('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum')], default='silver')
    vip_notes = fields.Text()


class HospitalPatientProfile(models.Model):
    """Delegation inheritance demo: profile owns one patient and exposes patient fields."""
    _name = 'hospital.patient.profile'
    _description = 'Patient Profile Delegation Demo'
    _inherits = {'hospital.patient': 'patient_id'}

    patient_id = fields.Many2one('hospital.patient', required=True, ondelete='cascade')
    profile_code = fields.Char(default='PROFILE')
    profile_notes = fields.Text()
