from odoo import http

class MainController(http.Controller):
    @http.route('/news', type='http', auth='public', website=True)
    def index(self):
        return "Welcome to My Module!"

