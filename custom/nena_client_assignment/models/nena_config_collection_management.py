from odoo import models, fields, api

class NenaConfigCollectionManagement(models.Model):
    _name = "nena.config.collection.management"
    _description = 'Configuración de Gestión de Cobranza'

    name = fields.Char(string='Nombre', required=True)
    max_credit_limit = fields.Float(string='Límite Máximo de Crédito', default=0, required=True)
    max_permit_overdraft = fields.Float(string='Monto Máximo de Permiso', default=0, required=True)
    allow_permit_overdraft = fields.Boolean(string='Permitir Otorgar Permiso', default=False)
    notes = fields.Text(string='Notas Adicionales')

    employee_ids = fields.One2many("hr.employee", "nena_config_collection_management_id", string="Empleado")
    