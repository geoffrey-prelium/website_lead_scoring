from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    website_lead_score = fields.Integer(
        string='Website Lead Score',
        default=0,
        readonly=True,
        help='Accumulated score based on website page views.'
    )

    def update_lead_score(self, score_delta):
        """
        Updates the lead score and checks for threshold crossings.
        """
        for partner in self:
            if score_delta == 0:
                continue
            
            old_score = partner.website_lead_score
            new_score = old_score + score_delta
            partner.website_lead_score = new_score

            # Check thresholds
            config = self.env['res.config.settings'].get_values()
            # Note: get_values() returns a dict, but for efficient threshold checking 
            # we should probably use ir.config_parameter directly or a cached method.
            # Using ir.config_parameter for performance.
            
            ICP = self.env['ir.config_parameter'].sudo()
            lead_threshold = int(ICP.get_param('website_lead_scoring.lead_threshold', 0))
            mql_threshold = int(ICP.get_param('website_lead_scoring.mql_threshold', 0))
            alert_user_id = int(ICP.get_param('website_lead_scoring.alert_user_id', 0))

            if lead_threshold > 0 and old_score < lead_threshold <= new_score:
                partner._on_lead_threshold_reached(alert_user_id, 'Lead')
            
            if mql_threshold > 0 and old_score < mql_threshold <= new_score:
                partner._on_lead_threshold_reached(alert_user_id, 'MQL')

    def _on_lead_threshold_reached(self, user_id, level):
        """
        Trigger actions when a threshold is reached.
        """
        self.ensure_one()
        msg = f"Partner {self.name} has reached the {level} threshold (Score: {self.website_lead_score})."
        
        # Log in chatter
        self.message_post(body=msg, subtype_xmlid='mail.mt_note')

        # Notify user if configured
        if user_id:
            user = self.env['res.users'].browse(user_id)
            if user.exists():
                self.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=user_id,
                    summary=f'New {level}: {self.name}',
                    note=msg
                )
