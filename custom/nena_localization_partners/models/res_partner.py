from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NenaResPartnerVe(models.Model):
    _inherit = "res.partner"

    # Dirección fiscal
    fiscal_state_id = fields.Many2one("nena.res.state.ve", string="Fiscal State")
    fiscal_state_name = fields.Char(related="fiscal_state_id.name", string="Fiscal State Name", store=True)

    fiscal_municipality_id = fields.Many2one("nena.res.state.municipality.ve", string="Fiscal Municipality")
    fiscal_municipality_name = fields.Char(related="fiscal_municipality_id.name", string="Fiscal Municipality Name", store=True)

    fiscal_city_id = fields.Many2one("nena.res.state.municipality.city.ve", string="Fiscal City")
    fiscal_city_name = fields.Char(related="fiscal_city_id.name", string="Fiscal City Name", store=True)

    # Dirección municipal (solo aplica si es cliente)
    municipal_state_id = fields.Many2one("nena.res.state.ve", string="Municipal State")
    municipal_state_name = fields.Char(related="municipal_state_id.name", string="Municipal State Name", store=True)

    municipal_municipality_id = fields.Many2one("nena.res.state.municipality.ve", string="Municipal Municipality")
    municipal_municipality_name = fields.Char(related="municipal_municipality_id.name", string="Municipal Municipality Name", store=True)

    municipal_city_id = fields.Many2one("nena.res.state.municipality.city.ve", string="Municipal City")
    municipal_city_name = fields.Char(related="municipal_city_id.name", string="Municipal City Name", store=True)

    @api.constrains("municipal_state_id", "municipal_municipality_id", "municipal_city_id")
    def _check_municipal_fields_for_customer(self):
        for partner in self:
            if not partner.customer_rank and (
                partner.municipal_state_id or partner.municipal_municipality_id or partner.municipal_city_id
            ):
                raise ValidationError("Municipal address fields can only be set for customers.")