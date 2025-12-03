from odoo import models, fields, api
import re

import logging

_logger = logging.getLogger(__name__)


class NenaRecord(models.Model):
    _name = "nena.record"
    _description = "Record Partner"

    res_partner_id = fields.Many2one("res.partner", copy=False)
    status_record_id = fields.Many2one("nena.gen.status", string="Status Postulation", domain=[('category', '=', 'EXPEDIENTE')])

    # Tipo de Postulacion
    postulation_type_id = fields.Many2one("nena.postulation.type")
    postulation_name = fields.Char(related="postulation_type_id.name")

    # Monitor de Postulaciones
    monitor_id = fields.Many2one("nena.postulation.monitor")
    monitor_sales = fields.Boolean(related="monitor_id.sales")
    monitor_regency = fields.Boolean(related="monitor_id.regency")
    monitor_legal = fields.Boolean(related="monitor_id.legal")
    monitor_payment = fields.Boolean(related="monitor_id.payment")

    # Datos de Cabecera
    partner_code = fields.Integer(string="Contact")
    name = fields.Char(string="Name", required=True)
    nena_ref = fields.Char(string="Reference", size=6)

    _sql_constraints = [
        (
            "nena_ref_unique",
            "UNIQUE(nena_ref)",
            "La Referencia del Expediente debe ser única.",
        )
    ]

    rif_type_id = fields.Many2one(
        "nena.type.identification", string="RIF", required=True
    )
    rif_number = fields.Char(size=9, required=True)

    rif = fields.Char(
        string="RIF",
        compute="_compute_rif",
        store=True,
        readonly=False,
        inverse="_inverse_rif",
    )
    industry_id = fields.Many2one("res.partner.industry", string="Industry")
    status_id = fields.Many2one("nena.gen.status", string="Status", domain="[('category', 'in', ['CLIENTE','PROVEEDOR'])]")
    cause_status_id = fields.Many2one("nena.cause.status", domain="[('gen_status_id', '=', status_id)]")
    zone_id = fields.Many2one("nena.zone", string="Zone")
    region_id = fields.Many2one("nena.region", string="Region")
    district_id = fields.Many2one("nena.district", string="District")

    # Datos Generales
    company_name = fields.Char(string="Company Name (RIF)")
    clasification_id = fields.Many2one(
        "nena.customer.clasification", string="Classification"
    )

    headquarters = fields.Selection(
        [("DUAL", "DUAL"), ("DN", "BARQUISIMETO"), ("DC", "GUARENA")],
        string="Headquarters",
        default="DN",
    )

    address_fiscal = fields.Text(string="Fiscal Directorate")
    state_fiscal_id = fields.Many2one("nena.res.state.ve", string="State")
    municipality_fiscal_id = fields.Many2one(
        "nena.res.state.municipality.ve", string="Municipality"
    )
    city_fiscal_id = fields.Many2one(
        "nena.res.state.municipality.city.ve", string="City"
    )
    address = fields.Text(string="Delivery Address")
    state_id = fields.Many2one("nena.res.state.ve", string="State")
    municipality_id = fields.Many2one(
        "nena.res.state.municipality.ve", string="Municipality"
    )
    city_id = fields.Many2one("nena.res.state.municipality.city.ve", string="City")
    zip_code = fields.Char(string="Zip Code")
    email_main = fields.Char(string="Main Email")
    email_secondary = fields.Char(string="Secondary Email")
    main_phone = fields.Char(string="Landline Telephone")
    main_mobile_phone = fields.Char(string="Mobile Phone")
    product_category_id = fields.Many2many(
        "product.category", string="Product Category"
    )
    account_payment_term_id = fields.Many2one("account.payment.term")

    # Datos Anexos (Condiciones)
    condition_ids = fields.Many2many(
        "nena.customer.condition",
        "nena_record_condition_rel",
        "partner_id",
        "condition_id",
        string="Rights",
    )

    # Ventas
    customer_category_id = fields.Many2one("nena.customer.category", string="Category")
    additional_days = fields.Integer(string="Miscellaneous Days")
    sales_commercial_discount = fields.Float(string="Trade Discount")
    ufi_club = fields.Boolean(string="UFI Club", default=False)

    # Cobranzas
    payment_type_id = fields.Many2one("nena.payment.type", string="Payment Type")
    days_inactive = fields.Integer(string="Days to Deactivate", default=0)
    chain_id = fields.Many2one("nena.chain", string="Chain")
    customer_credit_id = fields.Many2one("nena.credit.conditions.customer")
    customer_credit_limit = fields.Float(
        string="Credit Limit", related="customer_credit_id.credit_limit", readonly=False
    )
    customer_credit_balance = fields.Float(
        string="Balance", related="customer_credit_id.balance"
    )
    customer_credit_prepaid = fields.Float(
        string="Prepaid Amount", related="customer_credit_id.prepaid_amount"
    )

    # Regencia
    regent_id = fields.Many2one("nena.regent", string="Regent", ondelete="restrict")
    regent_id_number = fields.Char(related="regent_id.full_id_number")
    regent_phone = fields.Char(related="regent_id.phone", readonly=False)
    regent_address = fields.Text(related="regent_id.address", readonly=False)
    regent_matric_msds = fields.Char(related="regent_id.matric_msds", readonly=False)
    regent_colfar = fields.Char(related="regent_id.colfar", readonly=False)
    regent_oper_min_start_date = fields.Date(
        related="regent_id.oper_min_start_date", readonly=False
    )
    regent_oper_min_end_date = fields.Date(
        related="regent_id.oper_min_end_date", readonly=False
    )
    regent_inprefa_code = fields.Char(related="regent_id.inprefa_code", readonly=False)
    regent_sicm_code = fields.Char(related="regent_id.sicm_code", readonly=False)
    regent_sicm_status = fields.Many2one(
        related="regent_id.sicm_status_id", readonly=False
    )
    regent_sada_code = fields.Char(related="regent_id.sada_code", readonly=False)
    regent_sada_status = fields.Many2one(
        related="regent_id.sada_status_id", readonly=False
    )

    _sql_constraints = [
        (
            "unique_regent_per_customer",
            "UNIQUE(regent_id)",
            "Este regente ya está asignado a otro Expediente.",
        )
    ]

    # Expediente Digital
    # def _customer_type_domain(self):
    #    return self.env.ref("nena_partner_config_record.postulation_type_2").id

    documents_customer_line_ids = fields.One2many(
        "nena.attachment.line",
        "nena_record_id",
        string="Documents",
        domain=[("postulation_type_id", "=", 2)],
    )

    # Valores por Defectos
    def default_get(self, vals):
        record = super(NenaRecord, self).default_get(vals)
        default_code = self.env.context.get("default_postulation_code")
        is_customer = False

        if default_code:
            postulation_type = self.env["nena.postulation.type"].search(
                [("code", "=", default_code)], limit=1
            )
            if postulation_type:
                record["postulation_type_id"] = postulation_type.id
                if default_code == "CLI":
                    is_customer = True

        # Valor por Defecto para Estatus del Expediente
        default_status_record_id = self.env.ref("nena_partner_record.exp_solicitud")
        if default_status_record_id:
            record["status_record_id"] = default_status_record_id.id

        # Valor por Defecto para Estatus & Causa Estatus
        if is_customer:
            default_status_id = self.env.ref("nena_partner_record.cli_nuevo")
            if default_status_id:
                record["status_id"] = default_status_id.id

            default_cause_status_id = self.env.ref("nena_partner_record.cliente_nuevo")
            if default_cause_status_id:
                record["cause_status_id"] = default_cause_status_id.id

            # Valor por Defecto para Cadena
            default_chain_codchain = self.env.ref("nena_partner_record.ninguna")
            if default_chain_codchain:
                record["chain_id"] = default_chain_codchain.id

        return record

    # Acciones al Registrar o Actualizar
    def create(self, vals):
        record = super(NenaRecord, self).create(vals)

        monitor_vals = {
            "record_id": record.id,
            "name": record.name,
            "postulation_type": record.postulation_name,
        }
        monitor = self.env["nena.postulation.monitor"].create(monitor_vals)
        record.monitor_id = monitor.id

        return record

    def write(self, vals):
        partner_exists = {rec.id: bool(rec.partner_code) for rec in self}
        old_status = {rec.id: rec.status_record_id.code for rec in self}
        record = super(NenaRecord, self).write(vals)
        status_record_published = self.env.ref("nena_partner_record.exp_publicado")

        for record in self:
            is_published = (
                record.status_record_id
                and record.status_record_id.code == status_record_published.code
            )
            partner_was_created = partner_exists.get(record.id)
            was_previously_published = (
                old_status.get(record.id) == status_record_published.code
            )

            if (
                is_published
                and not partner_was_created
                and not was_previously_published
            ):
                # Crear el registro en Contacto
                partner_vals = {
                    "name": record.name,
                    "complete_name": record.name,
                    "ref": record.nena_ref,
                    "vat": record.rif,
                    "street": record.address_fiscal,
                    "city": record.city_fiscal_id.name,
                    "zip": record.zip_code,
                    "email": record.email_main,
                    "phone": record.main_phone,
                    "mobile": record.main_mobile_phone,
                    "is_company": True,
                    "property_payment_term_id": record.account_payment_term_id,
                }

                try:
                    partner = self.env["res.partner"].create(partner_vals)
                    _logger.info(f"PARTNER PRINCIPAL CREADO CON ÉXITO: {partner.id}")

                    # Crear el Contacto Hijo (Dirección de Entrega)
                    delivery_vals = {
                        "parent_id": partner.id,
                        "type": "delivery",
                        "name": f"Entrega {record.name}",
                        "street": record.address,
                        "city": record.city_id.name,
                    }

                    delivery_partner = self.env["res.partner"].create(delivery_vals)
                    _logger.info(
                        f"CONTACTO HIJO (ENTREGA) CREADO CON ÉXITO: {delivery_partner.id}"
                    )

                    # Enlazar el Partner Principal al Nena.Record
                    record.with_context(skip_partner_sync=True).partner_code = (
                        partner.id
                    )

                except Exception as e:
                    _logger.exception(f"FALLO EN LA CREACIÓN DEL PARTNER: {e}")

                # Cambiar Estatus del Cliente
                postulation = record.postulation_type_id
                if postulation.code == "CLI":
                    active_status_record = self.env.ref(
                        "nena_partner_record.cli_activo"
                    )
                    record.write({"status_id": active_status_record.id})
                    active_cause_status_record = self.env.ref(
                        "nena_partner_record.activo_cliente_al_dia"
                    )
                    record.write({"cause_status_id": active_cause_status_record.id})

        return record

    # Niveles de Aprobación
    show_approve_buttons = fields.Boolean(
        string="Show Approve", compute="_compute_show_approve_button"
    )

    @api.depends(
        "monitor_id.sales",
        "monitor_id.regency",
        "monitor_id.legal",
        "monitor_id.payment",
        "status_record_id.code",
    )
    def _compute_show_approve_button(self):
        group_map = {
            "sales": "nena_record.group_nena_record_sales",
            "regency": "nena_record.group_nena_record_regency",
            "legal": "nena_record.group_nena_record_legal",
            "payment": "nena_record.group_nena_record_payment",
        }

        user_groups_xml_ids = self.env.user.groups_id.get_external_id().values()
        status_record_decline = self.env.ref("nena_partner_record.exp_rechazar")

        for record in self:
            record.show_approve_buttons = False
            if record.status_record_id.code == status_record_decline.code:
                continue

            if record.monitor_id:
                record.show_approve_buttons = (
                    (
                        group_map["sales"] in user_groups_xml_ids
                        and not record.monitor_id.sales
                    )
                    or (
                        group_map["regency"] in user_groups_xml_ids
                        and not record.monitor_id.regency
                    )
                    or (
                        group_map["legal"] in user_groups_xml_ids
                        and not record.monitor_id.legal
                    )
                    or (
                        group_map["payment"] in user_groups_xml_ids
                        and not record.monitor_id.payment
                    )
                )

    # Botones de Accion
    def action_approved(self):
        group_to_field_map = {
            "nena_record.group_nena_record_sales": "sales",
            "nena_record.group_nena_record_regency": "regency",
            "nena_record.group_nena_record_legal": "legal",
            "nena_record.group_nena_record_payment": "payment",
        }

        external_ids = self.env.user.groups_id.get_external_id()
        user_groups_xml_ids = list(external_ids.values())
        approveal_status_record = self.env.ref("nena_partner_record.exp_aprobar")
        published_status_record = self.env.ref("nena_partner_record.exp_publicado")
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
                update_vals = {field_to_update: True}
                record.monitor_id.write(update_vals)

            # 3. Marcamos el Expediente en proceso de Aprobacion
            record.write({"status_record_id": approveal_status_record.id})

            # 4. Verificar si se cumplen todos los Niveles de Aprobacion pata Publicar el Expediente
            monitor = record.monitor_id
            if monitor.sales and monitor.regency and monitor.legal and monitor.payment:
                record.write({"status_record_id": published_status_record.id})

        return True

    def action_refused(self):
        for record in self:
            update_status = self.env.ref("nena_partner_record.exp_rechazar")
            if update_status:
                record.write({"status_record_id": update_status.id})
        return True

    def action_open_credit_conditions(self):
        self.ensure_one()

        credit_record = self.customer_credit_id
        if not credit_record:
            credit_record = self.env["nena.credit.conditions.customer"].create(
                {
                    "code": self.nena_ref or "CC-001",
                    "name": self.name or "Nueva Condición",
                }
            )
            self.customer_credit_id = credit_record

        return {
            "name": "Condiciones Crediticias",
            "type": "ir.actions.act_window",
            "res_model": "nena.credit.conditions.customer",
            "view_mode": "form",
            "res_id": credit_record.id,
            "target": "new",
            "context": {"default_record_id": self.id},
        }

    # Funciones
    @api.onchange("name")
    def _onchange_name_uppercase(self):
        if self.name:
            self.name = self.name.upper()

    @api.onchange("company_name")
    def _onchange_company_name_uppercase(self):
        if self.company_name:
            self.company_name = self.company_name.upper()

    @api.depends("rif_type_id.name", "rif_number")
    def _compute_rif(self):
        for record in self:
            prefix = record.rif_type_id.name if record.rif_type_id else ""

            if prefix and record.rif_number:
                record.rif = prefix + (record.rif_number).strip()
            else:
                record.rif = False

    def _inverse_rif(self):
        RifType = self.env["nena.document.type"]

        for record in self:
            if record.rif and len(record.rif) > 1:
                full_rif = record.rif.upper().strip()
                possible_prefix = full_rif[0]
                rif_type_record = RifType.search(
                    [("name", "=", possible_prefix)], limit=1
                )

                if rif_type_record:
                    record.rif_type_id = rif_type_record.id
                    record.rif_number = full_rif[1:]
                else:
                    record.rif_type_id = False
                    record.rif_number = full_rif
            else:
                record.rif_type_id = False
                record.rif_number = False

    @api.constrains("rif_number")
    def _check_rif_number_is_numeric(self):
        numeric_pattern = re.compile(r"^\d*$")
        for record in self:
            if record.rif_number and not numeric_pattern.match(record.rif_number):
                raise models.ValidationError(
                    "El RIF solo debe contener dígitos numéricos (0-9)."
                )

    @api.onchange("zone_id")
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

    @api.constrains("email_main", "email_secondary")
    def _check_emails(self):
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        for record in self:
            for field_name in ["email_main", "email_secondary"]:
                email_value = getattr(record, field_name)
                if email_value and not re.match(email_regex, email_value):
                    field_string = self._fields[field_name].string
                    raise models.ValidationError(
                        f"El campo '{field_string}' tiene un formato de correo inválido."
                    )

    @api.constrains("main_phone", "main_mobile_phone")
    def _check_phone_format(self):
        phone_regex = (
            r"^\d{11}$"  # Acepta números con 11 dígitos -- Ejemplo válido: 04141234567
        )
        for record in self:
            for field_name in ["main_phone", "main_mobile_phone"]:
                value = getattr(record, field_name)
                if value and not re.match(phone_regex, value):
                    field_string = self._fields[field_name].string
                    raise models.ValidationError(
                        f"El campo '{field_string}' tiene un formato de teléfono inválido."
                    )

    @api.onchange("state_id")
    def _onchange_state_id(self):
        if self.state_id:
            self.municipality_id = False
            self.city_id = False

    @api.onchange("municipality_id")
    def _onchange_municipality_id(self):
        if self.municipality_id:
            self.city_id = False

    @api.onchange("state_fiscal_id")
    def _onchange_state_fiscal_id(self):
        if self.state_fiscal_id:
            self.municipality_fiscal_id = False
            self.city_fiscal_id = False

    @api.onchange("municipality_fiscal_id")
    def _onchange_municipality_fiscal_id(self):
        if self.municipality_fiscal_id:
            self.city_fiscal_id = False
