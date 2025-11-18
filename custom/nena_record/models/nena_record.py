from odoo import models, fields, api
import re

import logging
_logger = logging.getLogger(__name__)

class NenaRecord(models.Model):
    _name = "nena.record"
    _description = 'Expediente de Cliente y Proveedor (Heredado de res.partner)'
    
    res_partner_id = fields.Many2one('res.partner', copy=False)
    status_record_id = fields.Many2one('nena.gen.status', string="Estatus")

    # Tipo de Postulacion
    postulation_type_id = fields.Many2one('postulation.type')
    postulation_name = fields.Char(related='postulation_type_id.name')

    # Monitor de Postulaciones
    monitor_id = fields.Many2one('nena.postulation.monitor')
    monitor_sales = fields.Boolean(related='monitor_id.sales')
    monitor_regency = fields.Boolean(related='monitor_id.regency')
    monitor_legal = fields.Boolean(related='monitor_id.legal')
    monitor_payment = fields.Boolean(related='monitor_id.payment')

    # Datos de Cabecera
    partner_code = fields.Integer(string="Contacto")
    name = fields.Char(string="Nombre", required=True)
    nena_ref = fields.Char(string="Referencia", size=6)

    _sql_constraints = [
        (
            "nena_ref_unique", 
            "UNIQUE(nena_ref)", 
            "La Referencia del Expediente debe ser única.", 
        )
    ]

    rif_type_id = fields.Many2one('nena.document.type', string="RIF", required=True)
    rif_number = fields.Char(size=9, required=True)
    rif = fields.Char(string="RIF", compute='_compute_rif', store=True, readonly=False, inverse='_inverse_rif')
    industry_id = fields.Many2one('res.partner.industry', string="Industria")
    status_id = fields.Many2one('nena.gen.status', string="Estatus")
    cause_status_id = fields.Many2one('nena.cause.status')
    zone_id = fields.Many2one('nena.zone', string="Zona")
    region_id = fields.Many2one('nena.region', string="Region")
    district_id = fields.Many2one('nena.district', string="Distrito")

    # Datos Generales
    company_name = fields.Char(string="Razón Social (RIF)")
    clasification_id = fields.Many2one('nena.customer.clasification', string="Clasificación")

    headquarters = fields.Selection([
                                    ('DUAL', 'DUAL'), 
                                    ('DN', 'BARQUISIMETO'), 
                                    ('DC', 'GUARENA')
                                    ], string="Sede", default='DN')

    address_fiscal = fields.Text(string="Dirección Fiscal")
    state_fiscal_id = fields.Many2one('nena.res.state.ve', string="Estado")
    municipality_fiscal_id = fields.Many2one('nena.res.state.municipality.ve', string="Municipio")
    city_fiscal_id = fields.Many2one('nena.res.state.municipality.city.ve', string="Ciudad")
    address = fields.Text(string="Dirección Entrega")
    state_id = fields.Many2one('nena.res.state.ve', string="Estado")
    municipality_id = fields.Many2one('nena.res.state.municipality.ve', string="Municipio")
    city_id = fields.Many2one('nena.res.state.municipality.city.ve', string="Ciudad")
    zip_code = fields.Char(string="Codigo Postal")
    email_main = fields.Char(string="Email Principal")
    email_secondary = fields.Char(string="Email Secundario")
    main_phone = fields.Char(string="Teléfono Fijo")
    main_mobile_phone = fields.Char(string="Teléfono Móvil")
    product_category_id = fields.Many2many('product.category', string="Tipo Producto")
    account_payment_term_id = fields.Many2one('account.payment.term')

    # Datos Anexos (Condiciones)
    condition_ids = fields.Many2many(
        'nena.condition', 
        'nena_record_condition_rel', 
        'partner_id', 
        'condition_id', 
        string="Derechos"
    )

    # Ventas
    customer_category_id = fields.Many2one('nena.customer.category', string="Categoria")
    additional_days = fields.Integer(string="Dias Miscelaneos")
    sales_commercial_discount = fields.Float(string="Dcto Comercial")
    ufi_club = fields.Boolean(string="Club UFI", default=False)

    # Cobranzas
    payment_type_id = fields.Many2one('nena.payment.type', string="Tipo Pago")
    days_inactive = fields.Integer(string="Días Inactivar", default=0)
    chain_id = fields.Many2one('nena.chain', string="Cadena")
    client_credit_id = fields.Many2one('nena.client.credit.conditions')
    client_credit_limit = fields.Float(string="Límite de Crédito", related="client_credit_id.credit_limit", readonly=False)
    client_credit_balance = fields.Float(string="Saldo", related="client_credit_id.balance")
    client_credit_prepaid = fields.Float(string="Monto Prepagado", related="client_credit_id.prepaid_amount")

    # Regencia
    regent_id = fields.Many2one('nena.regent', string='Regente', ondelete='restrict')
    regent_id_number = fields.Char(related='regent_id.full_id_number')
    regent_phone = fields.Char(related='regent_id.phone', readonly=False)
    regent_address = fields.Text(related='regent_id.address', readonly=False)
    regent_matric_msds = fields.Char(related='regent_id.matric_msds', readonly=False)
    regent_colfar = fields.Char(related='regent_id.colfar', readonly=False)
    regent_oper_min_start_date = fields.Date(related='regent_id.oper_min_start_date', readonly=False)
    regent_oper_min_end_date = fields.Date(related='regent_id.oper_min_end_date', readonly=False)
    regent_inprefa_code = fields.Char(related='regent_id.inprefa_code', readonly=False)
    regent_sicm_code = fields.Char(related='regent_id.sicm_code', readonly=False)
    regent_sicm_status = fields.Many2one(related='regent_id.sicm_status_id', readonly=False)
    regent_sada_code = fields.Char(related='regent_id.sada_code', readonly=False)
    regent_sada_status = fields.Many2one(related='regent_id.sada_status_id', readonly=False)
    
    _sql_constraints = [
        ('unique_regent_per_client', 'UNIQUE(regent_id)', 'Este regente ya está asignado a otro Expediente.')
    ]

    # Expediente Digital
    def _customer_type_domain(self):
        return self.env.ref('nena_partner_config_record.postulation_type_2').id

    documents_client_line_ids = fields.One2many('nena.attachment.line', 'nena_record_id', 
        string="Documentos", 
        domain=[('postulation_type_id', '=', 2)] #_customer_type_domain)]
    )

    # Valores por Defectos
    def default_get(self, vals):
        record = super(NenaRecord, self).default_get(vals)
        default_code = self.env.context.get('default_postulation_code')
        es_cliente = False
        
        if default_code:
            postulation_type = self.env['postulation.type'].search([('code', '=', default_code)], limit=1)
            if postulation_type:
                record['postulation_type_id'] = postulation_type.id
                if default_code == 'CLI':
                    es_cliente = True

        # Valor por Defecto para Estatus del Expediente
        default_status_record_code = 'EXP-01'
        new_status_record = self.env['nena.gen.status'].search([('code', '=', default_status_record_code)], limit=1)
        if new_status_record:
            record['status_record_id'] = new_status_record.id 

        # Valor por Defecto para Estatus & Causa Estatus
        if es_cliente:
            default_status_code = 'CLI-01'
            new_status = self.env['nena.gen.status'].search([('code', '=', default_status_code)], limit=1)
            if new_status:
                record['status_id'] = new_status.id

            default_cause_status_code = '007'
            new_cause_status = self.env['nena.cause.status'].search([('code', '=', default_cause_status_code)], limit=1)
            if new_cause_status:
                record['cause_status_id'] = new_cause_status.id
        
            # Valor por Defecto para Cadena
            default_chain_codchain = '0001'
            new_chain = self.env['nena.chain'].search([('codchain', '=', default_chain_codchain)], limit=1)
            if new_chain:
                record['chain_id'] = new_chain.id 

        return record

    # Acciones al Registrar o Actualizar
    def create(self, vals):
        record = super(NenaRecord, self).create(vals)

        monitor_vals = {
            'record_id': record.id,
            'name': record.name,
            'postulation_type': record.postulation_name
        }

        monitor = self.env['nena.postulation.monitor'].create(monitor_vals)
        record.monitor_id = monitor.id
        
        return record

    def write(self, vals):
        partner_exists = {rec.id: bool(rec.partner_code) for rec in self}
        old_status = {rec.id: rec.status_record_id.code for rec in self}
        record = super(NenaRecord, self).write(vals)

        for record in self:
            is_published = record.status_record_id and record.status_record_id.code == 'EXP-04'
            partner_was_created = partner_exists.get(record.id)
            was_previously_published = old_status.get(record.id) == 'EXP-04'

            if is_published and not partner_was_created and not was_previously_published:
                # Crear el registro en Contacto
                partner_vals = {
                        'name': record.name, 
                        'complete_name': record.name, 
                        'ref': record.nena_ref, 
                        'vat': record.rif, 
                        'street': record.address_fiscal, 
                        'city': record.city_fiscal_id.name, 
                        'zip': record.zip_code,
                        'email': record.email_main, 
                        'phone': record.main_phone, 
                        'mobile': record.main_mobile_phone, 
                        'is_company': True,
                        'property_payment_term_id': account_payment_term_id,
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
                        'city': record.city_id.name, 
                    }
                
                    delivery_partner = self.env['res.partner'].create(delivery_vals)
                    _logger.info(f'CONTACTO HIJO (ENTREGA) CREADO CON ÉXITO: {delivery_partner.id}')

                    # Enlazar el Partner Principal al Nena.Record
                    record.with_context(skip_partner_sync=True).partner_code = partner.id
                
                except Exception as e:
                    _logger.exception(f'FALLO EN LA CREACIÓN DEL PARTNER: {e}')

                # Cambiar Estatus del Cliente
                postulation = record.postulation_type_id
                if postulation.code == 'CLI':
                    active_status_record = self.env['nena.gen.status'].search([('code', '=', 'CLI-02')], limit=1)
                    record.write({'status_id': active_status_record.id})
                    active_cause_status_record = self.env['nena.cause.status'].search([('code', '=', '008')], limit=1)
                    record.write({'cause_status_id': active_cause_status_record.id})

        return record

    # Niveles de Aprobación
    show_approve_buttons = fields.Boolean(string="Mostrar Aprobar", compute='_compute_show_approve_button')

    @api.depends('monitor_id.sales', 'monitor_id.regency', 'monitor_id.legal', 'monitor_id.payment', 'status_record_id.code')
    def _compute_show_approve_button(self):
        group_map = {
            'sales': 'nena_record.group_nena_record_sales',
            'regency': 'nena_record.group_nena_record_regency',
            'legal': 'nena_record.group_nena_record_legal',
            'payment': 'nena_record.group_nena_record_payment',
        }

        user_groups_xml_ids = self.env.user.groups_id.get_external_id().values()

        for record in self:
            record.show_approve_buttons = False
            if record.status_record_id.code == 'EXP-03':
                continue

            if record.monitor_id:
                record.show_approve_buttons = (
                    (group_map['sales'] in user_groups_xml_ids and not record.monitor_id.sales) or
                    (group_map['regency'] in user_groups_xml_ids and not record.monitor_id.regency) or
                    (group_map['legal'] in user_groups_xml_ids and not record.monitor_id.legal) or
                    (group_map['payment'] in user_groups_xml_ids and not record.monitor_id.payment)
                )
            
    # Botones de Accion
    def action_approved(self):
        group_to_field_map = {
            'nena_record.group_nena_record_sales': 'sales',
            'nena_record.group_nena_record_regency': 'regency',
            'nena_record.group_nena_record_legal': 'legal',
            'nena_record.group_nena_record_payment': 'payment',
        }
        
        external_ids = self.env.user.groups_id.get_external_id()
        user_groups_xml_ids = list(external_ids.values())
        approveal_status_record = self.env['nena.gen.status'].search([('code', '=', 'EXP-02')], limit=1)
        published_status_record = self.env['nena.gen.status'].search([('code', '=', 'EXP-04')], limit=1)
        update_vals = {}

        for record in self:
            if not record.monitor_id:
                continue

            # 1. Comprobar si el ID XML del grupo está en los grupos del usuario
            field_to_update = None
            for xml_id, field_name in group_to_field_map.items():
                if xml_id in user_groups_xml_ids:
                    field_to_update = field_name
                    break 
            
            # 2. Actualizar el monitor si se encontró un grupo
            if field_to_update:
                update_vals = {
                    field_to_update: True
                }
                record.monitor_id.write(update_vals)
                
            # 3. Marcamos el Expediente en proceso de Aprobacion
            record.write({'status_record_id': approveal_status_record.id})

            # 4. Verificar si se cumplen todos los Niveles de Aprobacion pata Publicar el Expediente
            monitor = record.monitor_id
            if monitor.sales and monitor.regency and monitor.legal and monitor.payment:
                record.write({'status_record_id': published_status_record.id})

        return True

    def action_refused(self):
        for record in self:
            status_refused = 'EXP-03'
            update_status = self.env['nena.gen.status'].search([('code', '=', status_refused)], limit=1)
            if update_status:
                record.write({'status_record_id': update_status.id})
        
        return True

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
    
    @api.constrains('email_main', 'email_secondary')
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