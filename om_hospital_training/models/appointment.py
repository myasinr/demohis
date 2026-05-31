# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'reference'
    _order = 'appointment_date desc, id desc'

    reference = fields.Char(default='New', readonly=True, copy=False, tracking=True)
    patient_id = fields.Many2one('hospital.patient', required=True, ondelete='restrict', tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', required=True, ondelete='restrict', tracking=True)
    appointment_date = fields.Datetime(default=fields.Datetime.now, tracking=True)
    appointment_end = fields.Datetime(string='End Time')
    duration_hours = fields.Float(default=1.0)
    notes = fields.Text()
    diagnosis = fields.Text(groups='om_hospital_training.group_hospital_doctor,om_hospital_training.group_hospital_manager')
    line_ids = fields.One2many('hospital.appointment.line', 'appointment_id', string='Prescription Lines')
    total_quantity = fields.Float(compute='_compute_total_quantity', store=True)
    total_amount = fields.Float(compute='_compute_total_amount', store=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    state = fields.Selection([
        ('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'),
        ('done', 'Done'), ('cancelled', 'Cancelled')
    ], default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or 'New'
        return super(HospitalAppointment, self).create(vals)

    @api.depends('line_ids.quantity')
    def _compute_total_quantity(self):
        for rec in self:
            rec.total_quantity = sum(rec.line_ids.mapped('quantity'))

    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('subtotal'))

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id and self.patient_id.doctor_id:
            self.doctor_id = self.patient_id.doctor_id

    @api.constrains('duration_hours')
    def _check_duration(self):
        for rec in self:
            if rec.duration_hours <= 0:
                raise ValidationError(_('Duration must be greater than zero.'))

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_start(self):
        self.write({'state': 'ongoing'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_set_draft(self):
        self.write({'state': 'draft'})


class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Prescription Line'

    appointment_id = fields.Many2one('hospital.appointment', required=True, ondelete='cascade')
    medicine_id = fields.Many2one('hospital.medicine', required=True, ondelete='restrict')
    quantity = fields.Float(default=1.0)
    price_unit = fields.Float()
    subtotal = fields.Float(compute='_compute_subtotal', store=True)
    note = fields.Char()

    @api.onchange('medicine_id')
    def _onchange_medicine_id(self):
        if self.medicine_id:
            self.price_unit = self.medicine_id.price

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.price_unit

    @api.constrains('quantity')
    def _check_quantity(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError(_('Prescription quantity must be greater than zero.'))
