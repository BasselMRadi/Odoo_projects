from odoo import models, fields, api

class RejectReason(models.TransientModel):
    _name = 'reject.reason'
    _description = 'Reject Reason'

    reason = fields.Text('Reason', required=True)


    def action_confirm(self):
        for rec in self:
            record = rec.env[rec._context.get('active_model')].browse(rec._context.get('active_ids'))
            if record:
                record.rejection_reason=rec.reason
                record.status='rejected'
