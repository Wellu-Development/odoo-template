from odoo import http


class PartnerPostulations(http.Controller):

    @http.route("/postulation/client", type="http", auth="public", website=True)
    def postulation_client_handler(self):
        return http.request.render("nena_postulation.client_postulation")
