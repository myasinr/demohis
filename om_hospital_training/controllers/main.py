# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class HospitalTrainingController(http.Controller):

    @http.route('/hospital/api/patients', type='json', auth='user', methods=['POST'], csrf=False)
    def get_patients(self, **kwargs):
        patients = request.env['hospital.patient'].search([], limit=20)
        return [{
            'id': p.id,
            'reference': p.reference,
            'name': p.name,
            'age': p.age,
            'state': p.state,
        } for p in patients]

    @http.route('/hospital/api/create_patient', type='json', auth='user', methods=['POST'], csrf=False)
    def create_patient(self, **kwargs):
        vals = {
            'name': kwargs.get('name') or 'API Patient',
            'mobile': kwargs.get('mobile') or '0000000000',
            'email': kwargs.get('email'),
        }
        patient = request.env['hospital.patient'].create(vals)
        return {'id': patient.id, 'reference': patient.reference, 'name': patient.name}
