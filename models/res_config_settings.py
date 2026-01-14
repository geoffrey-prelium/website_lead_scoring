from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    lead_scoring_lead_threshold = fields.Integer(
        string='Lead Threshold',
        config_parameter='website_lead_scoring.lead_threshold',
        default=25
    )
    lead_scoring_mql_threshold = fields.Integer(
        string='MQL Threshold',
        config_parameter='website_lead_scoring.mql_threshold',
        default=50
    )
    lead_scoring_alert_user_id = fields.Many2one(
        'res.users',
        string='Alert User',
        config_parameter='website_lead_scoring.alert_user_id'
    )
