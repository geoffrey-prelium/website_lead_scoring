import logging
from odoo import models, http
from odoo.http import request

_logger = logging.getLogger(__name__)

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _post_dispatch(cls, response):
        super(IrHttp, cls)._post_dispatch(response)
        
        # Logic adapted from website.ir_http._register_website_track
        website_page = False
        if hasattr(response, '_cached_page'):
            website_page = response._cached_page
        elif hasattr(response, 'qcontext'):
            main_object = response.qcontext.get('main_object')
            if main_object and getattr(main_object, '_name', False) == 'website.page':
                website_page = main_object

        if website_page and request and hasattr(request, 'website') and request.website:
            user = request.env.user
            is_public = user._is_public()
            
            if not is_public and website_page.lead_score > 0:
                partner = request.env.user.partner_id
                partner.sudo().update_lead_score(website_page.lead_score)
        
        return response
