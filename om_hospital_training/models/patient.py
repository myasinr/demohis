# -*- coding: utf-8 -*-
from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'reference'
    _order = 'id desc'

    reference = fields.Char(string='Patient ID', default='New', readonly=True, copy=False, tracking=True)
    name = fields.Char(required=True, tracking=True)
    date_of_birth = fields.Date(tracking=True)
    age = fields.Integer(compute='_compute_age', inverse='_inverse_age', store=True, tracking=True)
    age_group = fields.Selection([
        ('child', 'Child'),
        ('adult', 'Adult'),
        ('senior', 'Senior Citizen'),
    ], compute='_compute_age_group', store=True)
    estimated_birth_year = fields.Integer(string='Estimated Birth Year')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], tracking=True)
    blood_group = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'), ('o+', 'O+'), ('o-', 'O-'),
    ])
    mobile = fields.Char(tracking=True)
    email = fields.Char()
    emergency_contact = fields.Char()
    guardian_name = fields.Char()
    is_child = fields.Boolean(compute='_compute_is_child', store=True, tracking=True)
    note = fields.Text()
    medical_history = fields.Text(groups='om_hospital_training.group_hospital_doctor,om_hospital_training.group_hospital_manager')
    consent_html = fields.Html(string='Consent Notes')
    patient_photo = fields.Binary(string='Photo')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    user_id = fields.Many2one('res.users', string='Responsible User', default=lambda self: self.env.user, tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Primary Doctor', ondelete='restrict', tracking=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id')
    appointment_count = fields.Integer(compute='_compute_appointment_count')
    total_prescription_qty = fields.Float(compute='_compute_total_prescription_qty', store=True)
    tag_ids = fields.Many2many('hospital.patient.tag', 'hospital_patient_tag_rel', 'patient_id', 'tag_id', string='Tags / Diseases')
    last_appointment_date = fields.Date(compute='_compute_last_appointment_date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('registered', 'Registered'),
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True)

    _sql_constraints = [
        ('hospital_patient_reference_unique', 'unique(reference)', 'Patient reference must be unique.'),
        ('hospital_patient_mobile_email_check', "CHECK(mobile IS NOT NULL OR email IS NOT NULL)", 'Enter at least mobile or email.'),
    ]

    @api.model
    def create(self, vals):
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or 'New'
        rec = super(HospitalPatient, self).create(vals)
        rec.message_post(body=_('Patient created through overridden create() method.'))
        return rec

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'cancelled':
            for rec in self:
                if rec.state == 'discharged':
                    raise ValidationError(_('Discharged patient cannot be cancelled.'))
        return super(HospitalPatient, self).write(vals)

    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancelled'):
                raise ValidationError(_('Only draft or cancelled patients can be deleted. Archive instead.'))
        return super(HospitalPatient, self).unlink()

    @api.depends('date_of_birth', 'estimated_birth_year')
    def _compute_age(self):
        today_value = fields.Date.context_today(self)
        today_date = fields.Date.from_string(today_value) if isinstance(today_value, str) else today_value
        today_year = today_date.year
        for rec in self:
            if rec.date_of_birth:
                dob = fields.Date.from_string(rec.date_of_birth) if isinstance(rec.date_of_birth, str) else rec.date_of_birth
                rec.age = today_year - dob.year - ((today_date.month, today_date.day) < (dob.month, dob.day))
            elif rec.estimated_birth_year:
                rec.age = today_year - rec.estimated_birth_year
            else:
                rec.age = 0

    def _inverse_age(self):
        today_value = fields.Date.context_today(self)
        today_date = fields.Date.from_string(today_value) if isinstance(today_value, str) else today_value
        current_year = today_date.year
        for rec in self:
            if rec.age and not rec.date_of_birth:
                rec.estimated_birth_year = current_year - rec.age

    @api.depends('age')
    def _compute_is_child(self):
        for rec in self:
            rec.is_child = bool(rec.age and rec.age < 18)

    @api.depends('age')
    def _compute_age_group(self):
        for rec in self:
            if rec.age and rec.age < 18:
                rec.age_group = 'child'
            elif rec.age and rec.age >= 60:
                rec.age_group = 'senior'
            else:
                rec.age_group = 'adult'

    @api.depends('appointment_ids.state')
    def _compute_appointment_count(self):
        data = self.env['hospital.appointment'].read_group(
            [('patient_id', 'in', self.ids)], ['patient_id'], ['patient_id']
        )
        mapped = {row['patient_id'][0]: row['patient_id_count'] for row in data if row.get('patient_id')}
        for rec in self:
            rec.appointment_count = mapped.get(rec.id, 0)

    @api.depends('appointment_ids.line_ids.quantity')
    def _compute_total_prescription_qty(self):
        for rec in self:
            rec.total_prescription_qty = sum(rec.appointment_ids.mapped('line_ids.quantity'))

    def _compute_last_appointment_date(self):
        for rec in self:
            dates = rec.appointment_ids.mapped('appointment_date')
            rec.last_appointment_date = max(dates) if dates else False

    @api.onchange('date_of_birth', 'age')
    def _onchange_child_warning(self):
        if self.age and self.age < 18:
            self.is_child = True
            return {
                'warning': {
                    'title': _('Child Patient Policy'),
                    'message': _('Guardian name is recommended for child patients.'),
                }
            }
        self.is_child = False

    @api.onchange('doctor_id')
    def _onchange_doctor_department_note(self):
        if self.doctor_id and self.doctor_id.department_id:
            self.note = _('Primary department: %s') % self.doctor_id.department_id.name

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age < 0:
                raise ValidationError(_('Age cannot be negative.'))
            if rec.age > 130:
                raise ValidationError(_('Age cannot be greater than 130.'))

    @api.constrains('is_child', 'guardian_name')
    def _check_child_guardian(self):
        for rec in self:
            if rec.is_child and not rec.guardian_name:
                raise ValidationError(_('Guardian name is required for child patients.'))

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '[%s] %s' % (rec.reference or 'New', rec.name or '')))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', ('name', operator, name), ('reference', operator, name), ('mobile', operator, name)]
        records = self.search(domain + args, limit=limit)
        return records.name_get()

    @api.model
    def name_create(self, name):
        rec = self.create({'name': name, 'mobile': '0000000000'})
        return rec.name_get()[0]

    def action_register(self):
        self.write({'state': 'registered'})

    def action_admit(self):
        self.write({'state': 'admitted'})

    def action_discharge(self):
        self.write({'state': 'discharged'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_set_draft(self):
        self.write({'state': 'draft'})

    def action_view_appointments(self):
        self.ensure_one()
        action = self.env.ref('om_hospital_training.action_hospital_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {'default_patient_id': self.id, 'search_default_patient_id': self.id}
        return action

    def action_demo_orm_pipeline(self):
        """Small demo for students: search -> filtered -> mapped -> sorted."""
        appointments = self.env['hospital.appointment'].search([('patient_id', 'in', self.ids)])
        done_patient_names = appointments.filtered(lambda r: r.state == 'done').mapped('patient_id.name')
        newest = appointments.sorted(key=lambda r: r.create_date or fields.Datetime.now(), reverse=True)
        message = _('Done appointment patients: %s<br/>Newest appointment: %s') % (
            ', '.join(done_patient_names) or '-', newest[:1].reference if newest else '-'
        )
        self[:1].message_post(body=message)
        return True
