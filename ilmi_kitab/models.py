from openerp import models, fields, api
class ilmi_sale_order_unique(models.Model):
    _inherit='res.partner'
    _sql_constraints = [
    ('mobile', 'unique(mobile)', 'This Mobile number already exists!')
    ]

