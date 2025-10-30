from odoo import models, fields, api
import re

class NenaRecord(models.Model):
    _name = "nena.record"
    _description = 'Expediente de Cliente y Proveedor'
    
    _sql_constraints = [
        (
            'code_unique', 
            'unique(code)', 
            'El Codigo del Expediente debe ser único.'),
        (
            "ref_unique",
            "UNIQUE(ref)",
            "La Referencia del Expediente debe ser única.",
        )
    ]

    code = fields.Char(string="Código", required=True, size=6)
    name = fields.Char(string="Nombre", required=True)
    ref = fields.Char(string="Referencia", required=True, size=6)
    postulation_type_id = fields.Many2one('postulation.type')

    rif_prefix = fields.Selection([
        ('V', 'V'),  # Venezolano
        ('J', 'J'),  # Jurídico (Empresa)
        ('G', 'G'),  # Gubernamental
        ('E', 'E'),  # Extranjero
    ], string="Prefijo RIF", default='V')

    rif_number = fields.Char(string="Número RIF", size=9)
    rif = fields.Char(string="RIF", compute='_compute_rif', store=True, readonly=False, inverse='_inverse_rif')

    region_id = fields.Many2one('nena.region', string="Region")
    district_id = fields.Many2one('nena.district', string="Distrito")
    zone_id = fields.Many2one('nena.zone', string="Zona")
    status_id = fields.Many2one('nena.gen.status', string="Estatus")
    cause_status_id = fields.Many2one('nena.cause.status')

    # Clientes
    clasification_id = fields.Many2one('nena.client.clasification', string="Clasificación")
    customer_category_id = fields.Many2one('nena.customer.category', string="Categoria")
    chain_id = fields.Many2one('nena.chain', string="Cadena")

    # Localizacion
    address = fields.Char(string="Dirección Entrega")
    state_id = fields.Many2one('nena.res.state.ve', string="Estado")
    municipality_id = fields.Many2one('nena.res.state.municipality.ve', string="Municipio")
    city_id = fields.Many2one('nena.res.state.municipality.city.ve', string="Ciudad")

    address_fiscal = fields.Char(string="Dirección Fiscal")
    state_fiscal_id = fields.Many2one('nena.res.state.ve', string="Estado Fiscal")
    municipality_fiscal_id = fields.Many2one('nena.res.state.municipality.ve', string="Municipio Fiscal")
    city_fiscal_id = fields.Many2one('nena.res.state.municipality.city.ve', string="Ciudad Fiscal")

    # Condicion Crediticia
    client_credit_id = fields.Many2one('nena.client.credit.conditions', string='Condición Crediticia')

    # Datos Anexos (Condiciones)
    condition_ids = fields.Many2many(
        'nena.condition',
        'nena_record_condition_rel',
        'partner_id',
        'condition_id',
        string="Derechos"
    )

    def default_get(self, fields_list):
        res = super(NenaRecord, self).default_get(fields_list)

        # Valor por Defecto para Postulation Type
        postulation_code = self.env.context.get('default_postulation_code')
        if postulation_code:
            postulation_type = self.env['postulation.type'].search([('code', '=', postulation_code)], limit=1)
            if postulation_type:
                res['postulation_type_id'] = postulation_type.id

        # Valor por Defecto para Estatus & Causa Estatus
        default_status_description = 'NUEVO'
        new_status = self.env['nena.gen.status'].search([('description', '=', default_status_description)], limit=1)
        if new_status:
            res['status_id'] = new_status.id

        default_cause_status_description = 'Cliente Nuevo'
        new_cause_status = self.env['nena.cause.status'].search([('description', '=', default_cause_status_description)], limit=1)
        if new_cause_status:
            res['cause_status_id'] = new_cause_status.id
        
        return res

    def action_open_credit_conditions(self):
        self.ensure_one()

        credit_record = self.client_credit_id
        if not credit_record:
            credit_record = self.env['nena.client.credit.conditions'].create({
                'code': self.code or 'CC-001',
                'name': self.name or 'Nueva Condición' 
            })
            self.client_credit_id = credit_record
            
        return {
            'name': "Condiciones Crediticias", 
            'type': 'ir.actions.act_window',
            'res_model': 'nena.client.credit.conditions', 
            'view_mode': 'form',
            'res_id': credit_record.id, 
            'target': 'new', 
            'context': {
                'default_record_id': self.id
            }
        }

    @api.onchange('name')
    def _onchange_name_uppercase(self):
        if self.name:
            self.name = self.name.upper()

    @api.depends('rif_prefix', 'rif_number')
    def _compute_rif(self):
        # Concatena el prefijo y el número para formar el RIF completo
        for record in self:
            if record.rif_prefix and record.rif_number:
                record.rif = record.rif_prefix + (record.rif_number).strip()
            else:
                record.rif = False

    def _inverse_rif(self):
        # Divide el RIF completo en prefijo y número al guardarse
        for record in self:
            if record.rif and len(record.rif) > 1:
                record.rif_prefix = record.rif[0]
                record.rif_number = record.rif[1:]
            else:
                record.rif_prefix = False
                record.rif_number = False

    @api.constrains('rif_number')
    def _check_rif_number_is_numeric(self):
        numeric_pattern = re.compile(r'^\d*$')
        for record in self:
            if record.rif_number and not numeric_pattern.match(record.rif_number):
                raise models.ValidationError("El RIF solo debe contener dígitos numéricos (0-9).")

    @api.onchange('region_id')
    def _onchange_region_id(self):
        if self.region_id:
            self.district_id = False
            self.zone_id = False

    @api.onchange('district_id')
    def _onchange_district_id(self):
        if self.district_id:
            self.zone_id = False

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id:
            self.municipality_id = False
            self.city_id = False

    @api.onchange('municipality_id')
    def _onchange_municipality_id(self):
        if self.municipality_id:
            self.city_id = False

    @api.onchange('state_fiscal_id')
    def _onchange_state_fiscal_id(self):
        if self.state_fiscal_id:
            self.municipality_fiscal_id = False
            self.city_fiscal_id = False

    @api.onchange('municipality_fiscal_id')
    def _onchange_municipality_fiscal_id(self):
        if self.municipality_fiscal_id:
            self.city_fiscal_id = False