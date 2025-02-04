from odoo import http
import json

class ApiController(http.Controller):
    @http.route('/api/data', type='json', auth='user')
    def get_data(self):
        return {'data': 'This is API data'}
