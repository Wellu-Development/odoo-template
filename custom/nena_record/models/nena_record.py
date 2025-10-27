from odoo import models, fields, api

class NenaRecord(models.Model):
    _name = "nena.record"
    _description = 'Expediente de Cliente y Proveedor'

    code = fields.Char(string="Código", required=True)
    name = fields.Char(string="Nombre", required=True)
    ref = fields.Integer(string="Referencia", required=True)

    postulation_type_id = fields.Many2one('postulation.type')
    zone_id = fields.Many2one('nena.zone', string="Zona")
    status_id = fields.Many2one('nena.gen.status', string="Estatus")
    cause_status_id = fields.Many2one('nena.cause.status', string="Causa del Estatus")

    # Clientes
    clasification_id = fields.Many2one('nena.client.clasification', string="Clasificación")

    # Cobranzas
    chain_id = fields.Many2one('nena.chain', string="Cadena")
    payment_type_id = fields.Many2one('payment.type', string="Tipo Corte")

    condition_ids = fields.Many2many(
        'nena.condition',
        'record_condition_rel',
        'partner_id',
        'condition_id',
        string="Derechos"
    )

    @api.onchange('postulation_type_id')
    def _onchange_postulation_type_id(self):
        if self.postulation_type_id and self._origin.id:
            raise UserError("No puedes modificar el tipo de postulación.")