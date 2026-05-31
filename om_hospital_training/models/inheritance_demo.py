# -*- coding: utf-8 -*-
from odoo import fields, models


class HospitalPatientExtension(models.Model):
    """Extension inheritance: adds columns into hospital.patient table."""
    _inherit = 'hospital.patient'

    insurance_required = fields.Boolean(string='Insurance Required')
    insurance_policy_no = fields.Char(string='Insurance Policy No.')
    age_restricted = fields.Boolean(string='Age Restricted')


class HospitalVipPatient(models.Model):
    """Classical inheritance demo: new model reusing hospital.patient structure."""
    _name = 'hospital.vip.patient'
    _inherit = 'hospital.patient'
    _description = 'VIP Patient Demo Model'

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
