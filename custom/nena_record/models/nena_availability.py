from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NenaAvailability(models.Model):
    _name = "nena.availability"
    _sql_constraints = [
        (
            "chain_ids_unique",
            "UNIQUE(chain_ids)",
            "Solo puede existir in registro por cada cadena",
        )
    ]

    balance = fields.Float(string='Saldo')
    creditlimit = fields.Float(string='Límite de Crédito')
    permitamount = fields.Float(string='Monto Permiso')
    transitamount = fields.Float(string='Monto en Tránsito')
    prepaidamount = fields.Float(string='Monto Prepago')
    availabilityamount = fields.Float(string='Monto Disponible')

    chain_ids = fields.Many2one('nena.chain', string='Cadena')