# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HospitalBulkAssignDoctorWizard(models.TransientModel):
    _name = 'hospital.bulk.assign.doctor.wizard'
    _description = 'Bulk Assign Doctor Wizard'

    doctor_id = fields.Many2one('hospital.doctor', required=True)
    note = fields.Text(string='Internal Note')
    patient_count = fields.Integer(compute='_compute_patient_count')

    def _compute_patient_count(self):
        active_ids = self.env.context.get('active_ids') or []
        for rec in self:
            rec.patient_count = len(active_ids)

    def action_assign_doctor(self):
        active_ids = self.env.context.get('active_ids') or []
        if not active_ids:
            raise UserError(_('Please select at least one patient.'))
        patients = self.env['hospital.patient'].browse(active_ids).exists()
        for wizard in self:
            patients.write({'doctor_id': wizard.doctor_id.id})
            if wizard.note:
                patients.message_post(body=_('Doctor assigned through wizard: %s<br/>Note: %s') % (wizard.doctor_id.name, wizard.note))
        return {'type': 'ir.actions.act_window_close'}
