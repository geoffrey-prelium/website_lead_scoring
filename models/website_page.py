from odoo import models, fields

class WebsitePage(models.Model):
    _inherit = 'website.page'

    lead_score = fields.Integer(
        string='Lead Score',
        default=0,
        help='Score assigned to the visitor when they view this page.'
    )


