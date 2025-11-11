from odoo import models, fields, api
import re

import logging
_logger = logging.getLogger(__name__)

class NenaRecord(models.Model):
    _name = "nena.record"
    _description = 'Expediente de Cliente y Proveedor (Heredado de res.partner)'
    
    _sql_constraints = [
        (
            "nena_ref_unique",
            "UNIQUE(nena_ref)",
            "La Referencia del Expediente debe ser única.",
        )
    ]

# Campos
    res_partner_id = fields.Many2one('res.partner', string='Contacto', copy=False)
    status_record_id = fields.Many2one('nena.gen.status', string="Estatus Expediente")
    postulation_type_id = fields.Many2one('postulation.type')
    product_category_id = fields.Many2one('product.category')

    # Datos de Cabecera
    partner_code = fields.Integer(string="Código")
    name = fields.Char(string="Nombre", required=True)
    nena_ref = fields.Char(string="Referencia", required=True, size=6)
    rif_type_id = fields.Many2one('nena.document.type', required=True)
    rif_number = fields.Char(string="Número RIF", size=9, required=True)
    rif = fields.Char(string="RIF", compute='_compute_rif', store=True, readonly=False, inverse='_inverse_rif')
    status_id = fields.Many2one('nena.gen.status', string="Estatus")
    cause_status_id = fields.Many2one('nena.cause.status')
    zone_id = fields.Many2one('nena.zone', string="Zona")
    region_id = fields.Many2one('nena.region', string="Region")
    district_id = fields.Many2one('nena.district', string="Distrito")

    # Datos Generales
    company_name = fields.Char(string="Razón Social (RIF)", required=True)
    clasification_id = fields.Many2one('nena.client.clasification', string="Clasificación")

    headquarters = fields.Selection([
                                    ('DUAL', 'DUAL'), 
                                    ('DN', 'BARQUISIMETO'), 
                                    ('DC', 'GUARENA')
                                ], string="Sede", default='DN')

    address_fiscal = fields.Char(string="Dirección Fiscal")
    state_fiscal_id = fields.Many2one('nena.res.state.ve', string="Estado")
    municipality_fiscal_id = fields.Many2one('nena.res.state.municipality.ve', string="Municipio")
    city_fiscal_id = fields.Many2one('nena.res.state.municipality.city.ve', string="Ciudad")
    address = fields.Char(string="Dirección Entrega")
    state_id = fields.Many2one('nena.res.state.ve', string="Estado")
    municipality_id = fields.Many2one('nena.res.state.municipality.ve', string="Municipio")
    city_id = fields.Many2one('nena.res.state.municipality.city.ve', string="Ciudad")
    email_main = fields.Char(string="Email Principal",required=True)
    email_secondary = fields.Char(string="Email Secundario")
    main_phone = fields.Char(string="Teléfono Principal")
    main_mobile_phone = fields.Char(string="Teléfono Móvil")

    # Ventas
    customer_category_id = fields.Many2one('nena.customer.category', string="Categoria")
    additional_days = fields.Integer(string="Dias Miscelaneos")
    sales_commercial_discount = fields.Float(string="Dcto Comercial")
    ufi_club = fields.Boolean(string="Club UFI", default=False)

    # Cobranzas
    payment_type_id = fields.Many2one('nena.payment.type', string="Tipo Pago")
    days_inactive = fields.Integer(string="Días Inactivar", default=0)
    chain_id = fields.Many2one('nena.chain', string="Cadena")
    client_credit_id = fields.Many2one('nena.client.credit.conditions', string='Condición Crediticia')

    # Expediente Digital
    def _customer_type_domain(self):
        return self.env.ref('nena_partner_config_record.postulation_type_2').id

    documents_client_line_ids = fields.One2many('nena.attachment.line', 'nena_record_id', 
        string="Documentos",
        domain=[('postulation_type_id','=',2)]
    )

    # Datos Anexos (Condiciones)
    condition_ids = fields.Many2many(
        'nena.condition',
        'nena_record_condition_rel',
        'partner_id',
        'condition_id',
        string="Derechos"
    )

    #Regente Datos
    regent_id = fields.Many2one(
    'nena.regent',
    string='Regent',
    required=True,
    ondelete='restrict'
    )
    regent_id_number = fields.Char(related='regent_id.id_number',readonly=False)
    regent_phone = fields.Char(related='regent_id.phone',readonly=False)
    regent_address = fields.Text(related='regent_id.address',readonly=False)
    regent_matric_msds = fields.Char(related='regent_id.matric_msds',readonly=False)
    regent_colfar = fields.Char(related='regent_id.colfar',readonly=False)
    regent_oper_min_start_date = fields.Date(related='regent_id.oper_min_start_date',readonly=False)
    regent_oper_min_end_date = fields.Date(related='regent_id.oper_min_end_date',readonly=False)
    regent_inprefa_code = fields.Char(related='regent_id.inprefa_code',readonly=False)
    regent_sicm_code = fields.Char(related='regent_id.sicm_code',readonly=False)
    regent_sicm_status = fields.Char(related='regent_id.sicm_status',readonly=False)
    regent_sada_code = fields.Char(related='regent_id.sada_code',readonly=False)
    regent_sada_status = fields.Char(related='regent_id.sada_status',readonly=False)
    _sql_constraints = [
    ('unique_regent_per_client', 'UNIQUE(regent_id)', 'Este regente ya está asignado a otro Expediente.')
    ]

# Valores por Defectos
    def default_get(self, fields_list):
        res = super(NenaRecord, self).default_get(fields_list)
        default_code = self.env.context.get('default_postulation_code')
        es_cliente = False
        
        if default_code:
            postulation_type = self.env['postulation.type'].search([('code', '=', default_code)], limit=1)
            if postulation_type:
                res['postulation_type_id'] = postulation_type.id
                if default_code == 'CLI':
                    es_cliente = True

        # Valor por Defecto para Estatus del Expediente
        default_status_record_description = 'SOLICITUD'
        new_status_record = self.env['nena.gen.status'].search([('description', '=', default_status_record_description)], limit=1)
        if new_status_record:
            res['status_record_id'] = new_status_record.id 

        # Valor por Defecto para Estatus & Causa Estatus
        default_status_description = 'NUEVO'
        new_status = self.env['nena.gen.status'].search([('description', '=', default_status_description)], limit=1)
        if new_status:
            res['status_id'] = new_status.id

        if es_cliente:
            default_cause_status_description = 'Cliente Nuevo'
            new_cause_status = self.env['nena.cause.status'].search([('description', '=', default_cause_status_description)], limit=1)
            if new_cause_status:
                res['cause_status_id'] = new_cause_status.id
        
        return res

 # Acciones
    def write(self, vals):
        partner_exists = {rec.id: bool(rec.partner_code) for rec in self}
        old_status = {rec.id: rec.status_record_id.description for rec in self}
        res = super(NenaRecord, self).write(vals)

        for record in self:
            is_published = record.status_record_id and record.status_record_id.description == 'PUBLICADO'
            partner_was_created = partner_exists.get(record.id)
            was_previously_published = old_status.get(record.id) == 'PUBLICADO'

            if is_published and not partner_was_created and not was_previously_published:
                partner_vals = {
                        'name': record.name, 
                        'complete_name': record.name,
                        'ref': record.nena_ref,
                        'vat': record.rif,
                        'street': record.address_fiscal,
                        'email': record.email_main,
                        'phone': record.main_phone,
                        'mobile': record.main_mobile_phone,
                        'is_company': True,
                }
                
                try:
                    partner = self.env['res.partner'].create(partner_vals)
                    _logger.info(f'PARTNER PRINCIPAL CREADO CON ÉXITO: {partner.id}')

                    # Crear el Contacto Hijo (Dirección de Entrega)
                    delivery_vals = {
                        'parent_id': partner.id,
                        'type': 'delivery',
                        'name': f"Entrega {record.name}",
                        'street': record.address, 
                        #'city': record.city,
                    }
                
                    delivery_partner = self.env['res.partner'].create(delivery_vals)
                    _logger.info(f'CONTACTO HIJO (ENTREGA) CREADO CON ÉXITO: {delivery_partner.id}')

                    # Enlazar el Partner Principal al Nena.Record
                    record.with_context(skip_partner_sync=True).partner_code = partner.id
                
                except Exception as e:
                    _logger.exception(f'FALLO EN LA CREACIÓN DEL PARTNER: {e}')
        return res

    def action_open_credit_conditions(self):
        self.ensure_one()

        credit_record = self.client_credit_id
        if not credit_record:
            credit_record = self.env['nena.client.credit.conditions'].create({
                'code': self.nena_ref or 'CC-001',
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

# Funciones
    @api.onchange('name')
    def _onchange_name_uppercase(self):
        if self.name:
            self.name = self.name.upper()
    
    @api.onchange('company_name')
    def _onchange_company_name_uppercase(self):
        if self.company_name:
            self.company_name = self.company_name.upper()

    @api.depends('rif_type_id.name', 'rif_number')
    def _compute_rif(self):
        for record in self:
            prefix = record.rif_type_id.name if record.rif_type_id else ''
            
            if prefix and record.rif_number:
                record.rif = prefix + (record.rif_number).strip()
            else:
                record.rif = False

    def _inverse_rif(self):
        RifType = self.env['nena.document.type']

        for record in self:
            if record.rif and len(record.rif) > 1:
                full_rif = record.rif.upper().strip()
                possible_prefix = full_rif[0] 
                rif_type_record = RifType.search([('name', '=', possible_prefix)], limit=1)

                if rif_type_record:
                    record.rif_type_id = rif_type_record.id 
                    record.rif_number = full_rif[1:]
                else:
                    record.rif_type_id = False
                    record.rif_number = full_rif
            else:
                record.rif_type_id = False
                record.rif_number = False

    @api.constrains('rif_number')
    def _check_rif_number_is_numeric(self):
        numeric_pattern = re.compile(r'^\d*$')
        for record in self:
            if record.rif_number and not numeric_pattern.match(record.rif_number):
                raise models.ValidationError("El RIF solo debe contener dígitos numéricos (0-9).")

    @api.onchange('zone_id')
    def _onchange_zone_id_set_parent(self):
        for record in self:
            if record.zone_id:
                # Asignar el Distrito:
                district = record.zone_id.district_id
                record.district_id = district
                
                # Asignar la Región:
                if district:
                    record.region_id = district.region_id
                else:
                    record.region_id = False
            else:
                record.district_id = False
                record.region_id = False
    
    @api.constrains('email_main','email_secondary')
    def _check_emails(self):
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        for record in self:
            for field_name in ['email_main', 'email_secondary']:
                email_value = getattr(record, field_name)
                if email_value and not re.match(email_regex, email_value):
                    field_string = self._fields[field_name].string
                    raise models.ValidationError(f"El campo '{field_string}' tiene un formato de correo inválido.")
                
    @api.constrains('main_phone', 'main_mobile_phone')
    def _check_phone_format(self):
         phone_regex = r'^\d{11}$' # Acepta números con 11 dígitos -- Ejemplo válido: 04141234567
         for record in self:
             for field_name in ['main_phone', 'main_mobile_phone']:
                 value = getattr(record, field_name)
                 if value and not re.match(phone_regex, value):
                     field_string = self._fields[field_name].string
                     raise models.ValidationError(f"El campo '{field_string}' tiene un formato de teléfono inválido.")

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