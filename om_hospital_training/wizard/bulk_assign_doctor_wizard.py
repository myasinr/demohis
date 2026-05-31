# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class HospitalBulkAssignDoctorWizard(models.TransientModel):
    _name = 'hospital.bulk.assign.doctor.wizard'
    _description = 'Bulk Assign Doctor Wizard'

    doctor_id = fields.Many2one('hospital.doctor', required=True)
    remarks = fields.Text()

    def action_assign_doctor(self):
        active_ids = self.env.context.get('active_ids', [])
        patients = self.env['hospital.patient'].browse(active_ids)
        if not patients:
            raise UserError(_('Please select at least one patient.'))
        patients.write({'doctor_id': self.doctor_id.id})
        for patient in patients:
            patient.message_post(body=_('Doctor assigned in bulk: %s') % self.doctor_id.name)
        return {'type': 'ir.actions.act_window_close'}
