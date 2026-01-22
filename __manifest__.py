{
    'name': 'Website Lead Scoring',
    'version': '1.0',
    'author': 'Prelium',
    'category': 'Website',
    'summary': 'Score website visitors based on page views and convert to leads.',
    'description': """
        This module allows you to assign scores to website pages.
        When a tracked partner visits a page, their score increases.
        Thresholds can be configured to trigger Lead/MQL status updates.
    """,
    'depends': ['website', 'crm', 'contacts'],
    'data': [
        'data/ir.model.access.csv',
        'views/website_page_views.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
