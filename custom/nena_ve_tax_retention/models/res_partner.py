from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'  

    # ... (Campos vat, is_special_taxpayer existentes) ...

    # Nuevo Campo para REGISTRO DE RETENCIÓN DE COMPRAS
    # Esta regla indica la tasa que MI COMPAÑÍA debe aplicar a ESTE PROVEEDOR (75% o 100%)
    # Usamos un nombre claro para evitar confusiones con la retención que EL CLIENTE nos aplica.
    iva_purchase_retention_rule_id = fields.Many2one(
        'l10n_ve.tax.retention',
        string='Regla de Retención IVA (Compras)',
        domain="[('end_date', '=', False), ('retention_type', 'in', ['standard', 'penalty'])]",
        help="Regla de retención de IVA que su compañía aplica a este Proveedor (75% estándar o 100% punitiva)."
    )

    # Campo para REGISTRO DE RETENCIÓN DE VENTAS (Cuando el Cliente nos retiene)
    # Este campo es la regla que el CLIENTE (Partner) aplica a NUESTRA compañía (Sujeto Retenido).
    iva_sales_retention_rule_id = fields.Many2one(
        'l10n_ve.tax.retention',
        string='Regla de Retención IVA (Ventas)',
        domain="[('end_date', '=', False), ('retention_type', 'in', ['standard', 'penalty'])]",
        help="Regla de retención de IVA que aplica el Partner cuando actúa como Agente de Retención sobre nuestras ventas."
    )
    
    # ... (Otros métodos) ...