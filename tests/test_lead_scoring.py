from odoo.tests.common import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestLeadScoring(TransactionCase):

    def setUp(self):
        super(TestLeadScoring, self).setUp()
        self.website = self.env['website'].create({'name': 'Test Website'})
        self.page = self.env['website.page'].create({
            'url': '/test-score-page',
            'is_published': True,
            'website_id': self.website.id,
            'lead_score': 10,
        })
        self.partner = self.env['res.partner'].create({
            'name': 'Test Visitor',
            'email': 'visitor@example.com',
        })
        # Configure thresholds
        self.env['ir.config_parameter'].sudo().set_param('website_lead_scoring.lead_threshold', 20)
        self.env['ir.config_parameter'].sudo().set_param('website_lead_scoring.mql_threshold', 50)

    def test_score_update(self):
        """Test that calling update_lead_score increases the score."""
        self.partner.update_lead_score(10)
        self.assertEqual(self.partner.website_lead_score, 10)
        
        self.partner.update_lead_score(5)
        self.assertEqual(self.partner.website_lead_score, 15)

    def test_threshold_trigger(self):
        """Test that crossing a threshold triggers an activity/message."""
        # Set current user as alert user
        self.env['ir.config_parameter'].sudo().set_param('website_lead_scoring.alert_user_id', self.env.user.id)
        
        # Initial score 15
        self.partner.website_lead_score = 15
        
        # Increase to 25 (crosses Lead threshold 20)
        self.partner.update_lead_score(10)
        
        # Check messages
        messages = self.partner.message_ids
        self.assertTrue(any('Lead' in m.body for m in messages), "Should log a Lead message")
        
        # Check activity
        activities = self.env['mail.activity'].search([('res_id', '=', self.partner.id), ('res_model', '=', 'res.partner')])
        self.assertTrue(activities, "Should create an activity")
