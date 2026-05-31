# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class HospitalApiController(http.Controller):
    """Simple JSON controller for training integration concepts.

    Call with JSON-RPC style POST to /hospital/api/create_patient.
    Example params: {"name": "Ali", "mobile": "03000000000", "email": "a@test.com"}
    """

    @http.route('/hospital/api/create_patient', type='json', auth='user', methods=['POST'], csrf=False)
    def create_patient(self, **payload):
        vals = {
            'name': payload.get('name'),
            'mobile': payload.get('mobile'),
            'email': payload.get('email'),
            'gender': payload.get('gender'),
        }
        vals = {k: v for k, v in vals.items() if v}
        patient = request.env['hospital.patient'].sudo().create(vals)
        return {
            'id': patient.id,
            'reference': patient.reference,
            'name': patient.name,
        }
