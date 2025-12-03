from odoo import models, fields

class NenaChain(models.Model):
    _name = "nena.chain"
    _description = "Chain"
    _rec_name = "name"

    _sql_constraints = [
        ("name_unique", "unique(name)", "El nombre de la cadena debe ser único.")
    ]

    code = fields.Char(string="Code", size=4, required=True)
    name = fields.Char(string="Chain", required=True)
    commercialduct = fields.Float(string="Trade Discount")
    promptpaymentdiscount = fields.Float(string="Early Payment Discount")
    status_id = fields.Many2one("nena.gen.status", string="Status")
    cause_status_id = fields.Many2one("nena.cause.status")
    group_id = fields.Many2one("nena.group", string="Groups")
    customer_ids = fields.One2many("nena.record", "chain_id", string="Customer")

    # Condición Crediticia
    chain_credit_id = fields.Many2one("nena.credit.conditions.chain")
    chain_credit_limit = fields.Float(
        string="Credit Limit", related="chain_credit_id.credit_limit", readonly=False
    )
    chain_credit_balance = fields.Float(
        string="Balance", related="chain_credit_id.balance"
    )
    chain_credit_transit = fields.Float(
        string="Transit Amount", related="chain_credit_id.transit_amount"
    )
    chain_credit_prepaid = fields.Float(
        string="Prepaid Amount", related="chain_credit_id.prepaid_amount"
    )
    chain_credit_availability = fields.Float(
        string="Availability", related="chain_credit_id.availability_amount"
    )

    # Parametros de Cadena (Condiciones)
    condition_ids = fields.Many2many(
        "nena.customer.condition",
        "nena_chain_condition_rel",
        "partner_id",
        "condition_id",
        string="Parameters",
    )

    # Valores por Defectos
    def default_get(self, fields_list):
        res = super(NenaChain, self).default_get(fields_list)

        # Valor por Defecto para Estatus
        default_status_code = self.env.ref("nena_partner_record.cad_activo")
        if default_status_code:
            res["status_id"] = default_status_code.id

        default_cause_status_code = self.env.ref("nena_partner_record.activo_grupo_al_dia")
        if default_cause_status_code:
            res["cause_status_id"] = default_cause_status_code.id

        return res

    # Botones de Accion
    def action_open_credit_conditions(self):
        self.ensure_one()

        credit_record = self.chain_credit_id
        if not credit_record:
            credit_record = self.env["nena.credit.conditions.chain"].create(
                {
                    "code": self.code or "CA-001",
                    "name": self.name or "New Condition",
                }
            )
            self.chain_credit_id = credit_record

        return {
            "name": "Credit Conditions",
            "type": "ir.actions.act_window",
            "res_model": "nena.credit.conditions.chain",
            "view_mode": "form",
            "res_id": credit_record.id,
            "target": "new",
            "context": {"default_record_id": self.id},
        }
