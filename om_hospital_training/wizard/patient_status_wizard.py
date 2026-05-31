# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class HospitalPatientStatusWizard(models.TransientModel):
    _name = 'hospital.patient.status.wizard'
    _description = 'Patient Status Update Wizard'

    state = fields.Selection([
        ('draft', 'Draft'), ('registered', 'Registered'), ('admitted', 'Admitted'),
        ('discharged', 'Discharged'), ('cancelled', 'Cancelled')
    ], required=True)
    note = fields.Text()

    def action_update_status(self):
        patients = self.env['hospital.patient'].browse(self.env.context.get('active_ids', []))
        if not patients:
            raise UserError(_('Please select at least one patient.'))
        patients.write({'state': self.state})
        for patient in patients:
            patient.message_post(body=_('Status updated by wizard to: %s') % self.state)
        return {'type': 'ir.actions.act_window_close'}
