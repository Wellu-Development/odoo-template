from odoo import models, fields,api

class NenaProductClass(models.Model):
    _name = "nena.product.class"
    _description = "Nena Master Product Class"
    _rec_name = "description"
    _inherit = ['mail.thread','mail.activity.mixin']
    
    _sql_constraints = [
        (
            "code_description_unique",
            "UNIQUE(code,description,product_family_id)",
            "El código de la clase del producto debe de ser único",
        )
    ]
    
    code = fields.Char(string='Código', size=15,required=True, tracking=True)
    description = fields.Char(string='Descripción', size=80, required=True, tracking=True)
    product_family_id = fields.Many2one('nena.product.family', string="Familia", required=True, tracking=True)
    active = fields.Boolean(string='Activo',default=True, tracking=True)

     # Funciones
    @api.onchange('description')
    def _onchange_description_uppercase(self):
        if self.description:
            self.description = self.description.upper()

    @api.constrains('description')
    def _check_description_constraints(self):
        for record in self:
            if record.description:
                if len(record.description) > 80:
                    raise models.ValidationError("La descripción no puede tener más de 80 caracteres.")

