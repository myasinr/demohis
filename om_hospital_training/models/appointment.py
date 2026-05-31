# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'reference'
    _order = 'appointment_datetime desc, id desc'

    reference = fields.Char(default='New', readonly=True, copy=False, tracking=True)
    patient_id = fields.Many2one('hospital.patient', required=True, ondelete='restrict', tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', required=True, ondelete='restrict', tracking=True)
    department_id = fields.Many2one(related='doctor_id.department_id', store=True, readonly=True)
    appointment_date = fields.Date(default=fields.Date.context_today, tracking=True)
    appointment_datetime = fields.Datetime(default=fields.Datetime.now, tracking=True)
    duration_hours = fields.Float(default=1.0)
    reason = fields.Text()
    diagnosis = fields.Text(groups='om_hospital_training.group_hospital_doctor,om_hospital_training.group_hospital_manager')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True)
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High'), ('3', 'Critical')], default='1')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    line_ids = fields.One2many('hospital.appointment.line', 'appointment_id', string='Prescription Lines', copy=True)
    total_quantity = fields.Float(compute='_compute_total_quantity', store=True)
    total_amount = fields.Float(compute='_compute_total_amount', store=True)
    line_count = fields.Integer(compute='_compute_line_count')

    @api.model
    def create(self, vals):
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or 'New'
        rec = super(HospitalAppointment, self).create(vals)
        rec.message_post(body=_('Appointment created and sequence assigned.'))
        return rec

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'cancelled':
            for rec in self:
                if rec.state == 'done':
                    raise ValidationError(_('Done appointments cannot be cancelled.'))
        return super(HospitalAppointment, self).write(vals)

    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancelled'):
                raise ValidationError(_('Only draft or cancelled appointments can be deleted.'))
        return super(HospitalAppointment, self).unlink()

    @api.depends('line_ids.quantity')
    def _compute_total_quantity(self):
        for rec in self:
            rec.total_quantity = sum(rec.line_ids.mapped('quantity'))

    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('subtotal'))

    def _compute_line_count(self):
        for rec in self:
            rec.line_count = len(rec.line_ids)

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id and self.patient_id.doctor_id:
            self.doctor_id = self.patient_id.doctor_id

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        if self.doctor_id:
            self.department_id = self.doctor_id.department_id

    @api.constrains('duration_hours')
    def _check_duration(self):
        for rec in self:
            if rec.duration_hours <= 0:
                raise ValidationError(_('Appointment duration must be greater than zero.'))
            if rec.duration_hours > 12:
                raise ValidationError(_('Appointment duration cannot be greater than 12 hours.'))

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_start(self):
        self.write({'state': 'ongoing'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})


class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    appointment_id = fields.Many2one('hospital.appointment', required=True, ondelete='cascade')
    name = fields.Char(string='Medicine / Service', required=True)
    quantity = fields.Float(default=1.0)
    unit_price = fields.Float(default=0.0)
    subtotal = fields.Float(compute='_compute_subtotal', store=True)
    note = fields.Char()

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.unit_price

    @api.constrains('quantity')
    def _check_quantity(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError(_('Quantity must be greater than zero.'))
