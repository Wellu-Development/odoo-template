from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

COMPANY_TYPE = ("COMPANY", "PERSON")

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    record_id = fields.Many2one('nena.record', compute='compute_stage', string='Records') 
    res_partner_ids = fields.One2many('nena.record', 'res_partner_id') 
    person_type_id = fields.Many2one('nena.person.type', string='Type of Contact')
    rif_type_id = fields.Many2one('nena.document.type', string='RIF')
    rif_number = fields.Char(string="Number RIF", size=9, required=True)

    def js_attach_files(self, files):
        attachment = self.env["ir.attachment"].create(
            [
                {
                    "name": file[0]["name"],
                    "datas": file[0]["data"],
                    "res_model": self._name,
                    "res_id": self.id,
                }
                for file in files.values()
            ]
        )

        return attachment.ids

    def js_create_partners(self, data, files):
        vals = dict()

        for key, value in data.items():
            preffix, suffix = key.split("_", 1)

            if preffix not in vals:
                vals.update({preffix: dict()})

            vals[preffix][suffix] = value

        partners = self.sudo().create(
            [{"company_type": key, **value} for key, value in vals.items()]
        )

        company = partners[0]
        person = partners[1]

        person.parent_id = company.id

        company.js_attach_files(files)

        return partners.read()

    def js_create_customer(self, data, files):
        return self.js_create_partners(data, files)

    def js_create_supplier(self, data, files):
        return self.js_create_partners(data, files)