from odoo import models, fields,api

class NenaProductFamily(models.Model):
    _name = "nena.product.family"
    _description = "Product Family"
    _rec_name = "description"
    _inherit = ['mail.thread','mail.activity.mixin']

    _sql_constraints = [
         (
             "code_description_unique",
             "UNIQUE(code,description,product_subtype_id)",
             "El código de la familia del producto debe de ser único",
         )
    ]

    code = fields.Char(string='Code', size=15,required=True, tracking=True)
    description = fields.Char(string='Description', size=80, required=True, tracking=True)
    product_subtype_id = fields.Many2one('nena.product.subtype', string="Subtype",tracking=True)
    active = fields.Boolean(string='Active',default=True, tracking=True)

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