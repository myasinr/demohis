# Odoo v13 Training - Hospital Management

This package contains one installable Odoo 13 module: `om_hospital_training`.

## Covered Concepts

- Module manifest, init files, data loading order
- Models, fields, defaults, reserved fields, rec_name, SQL constraints
- Many2one, One2many, Many2many
- Computed fields, inverse fields, onchange, Python constraints
- create(), write(), unlink(), name_get(), name_search(), name_create()
- read_group(), mapped(), filtered(), sorted()
- Tree, form, search, kanban, calendar, graph and pivot views
- Odoo v13 attrs, states, statusbar, chatter and smart buttons
- Security groups, ACLs, record rules and field-level security
- Extension, classical and delegation inheritance demos
- TransientModel wizards, active_ids and batch processing
- QWeb PDF reports
- JSON controller examples

## Install

Copy `om_hospital_training` into your Odoo 13 custom addons path, restart Odoo, update Apps List, and install **Odoo v13 Training - Hospital Management**.

Recommended command line:

```bash
python odoo-bin -d your_db -u om_hospital_training -c odoo.conf
```

## Notes

This module is designed for classroom practice. It avoids Odoo 17/19-only XML modifiers and uses Odoo 13 compatible `attrs` and `states` patterns.
