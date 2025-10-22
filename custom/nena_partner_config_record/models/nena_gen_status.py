from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class NenaGenStatus (models.Model):

    _name = "nena.gen.status"
    _description = "General Status"
    _rec_name = "description"
    
    description = fields.Text(required=True)

    postulation_type_id = fields.Many2one('postulation.type')

    

    @api.constrains('description')
    def _check_description_constraints(self):
        for record in self:
            if record.description:
                # Validar longitud máxima
                if len(record.description) > 50:
                    raise ValidationError("La descripción no puede tener más de 50 caracteres.")
                # Validar que no contenga números
                if re.search(r'\d', record.description):
                    raise ValidationError("La descripción no puede contener números.")


    