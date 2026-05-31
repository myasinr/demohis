# Odoo 13 Hospital Training Project

This module is a complete practical training project for Odoo v13 learners. It is designed to demonstrate the concepts covered in the Odoo development workshop slides through running examples.

## Module Name

`om_hospital_training`

## Tested Target

- Odoo Community/Enterprise 13.0
- Python 3.6 / 3.7 environment normally used for Odoo 13
- PostgreSQL database

## Dependencies

- `base`
- `mail`

## What Students Can Practice

### 1. Models and Fields
- Char, Text, Html, Integer, Float, Boolean, Date, Datetime, Selection, Binary
- `_name`, `_description`, `_rec_name`, `_order`
- `active` archive/unarchive behavior
- reserved audit fields such as create_uid, create_date, write_uid, write_date

### 2. Relationships
- Many2one: Patient to Doctor, Appointment to Patient
- One2many: Patient to Appointments, Appointment to Lines
- Many2many: Patient to Tags/Diseases
- ondelete behavior: restrict and cascade

### 3. Data Control
- Computed fields with `@api.depends`
- Stored computed fields with `store=True`
- Inverse method demo through age and estimated birth year
- Onchange methods with warnings
- Python constraints with `@api.constrains`
- SQL constraints using `_sql_constraints`

### 4. Views and UI
- Tree/List view
- Form view with header, statusbar, buttons, notebook tabs, groups
- Search view with filters and group by
- Kanban view with QWeb template
- Calendar view
- Graph view
- Pivot view
- Smart buttons
- Chatter

### 5. Security
- Security groups: Receptionist, Doctor, Hospital Manager
- ACLs in `ir.model.access.csv`
- Record rules for multi-company and receptionist ownership
- Field-level security for medical history and diagnosis

### 6. ORM Mastery
- create(), write(), unlink() overrides
- search(), browse(), read_group(), mapped(), filtered(), sorted()
- name_get(), name_search(), name_create()
- action dictionaries and smart buttons

### 7. Enterprise Patterns
- Sequence generation with `ir.sequence`
- `noupdate="1"` protected configuration data
- Wizard using `models.TransientModel`
- `active_ids` batch processing
- QWeb PDF report
- JSON controller endpoint
- Inheritance demo: extension, classical, and delegation inheritance

## Installation

1. Copy the folder `om_hospital_training` into your custom addons path.
2. Restart Odoo.
3. Activate Developer Mode.
4. Update Apps List.
5. Search for **Odoo 13 Hospital Training Project**.
6. Install the module.

Command-line upgrade example:

```bash
./odoo-bin -c odoo.conf -d your_database -u om_hospital_training
```

## Main Menus

- Hospital Training / Operations / Patients
- Hospital Training / Operations / Appointments
- Hospital Training / Configuration / Departments
- Hospital Training / Configuration / Doctors
- Hospital Training / Reporting / Patient Analysis
- Hospital Training / Reporting / Appointment Analysis
- Hospital Training / Architecture Demos

## Important Teaching Notes

- Use Patients to teach field types, chatter, constraints, workflows, smart buttons and reporting.
- Use Appointments to teach Many2one, One2many, computed totals, calendar, kanban, graph and pivot.
- Use the Bulk Assign Doctor wizard from the Patient list Action menu to teach TransientModel and active_ids.
- Use the Architecture Demos menu to explain inheritance patterns.
- Use groups and record rules to demonstrate why hiding menus is not real security.

## Known Intentional Simplification

This is a classroom module, not a medical production system. It is intentionally simplified so students can see Odoo framework concepts clearly.
