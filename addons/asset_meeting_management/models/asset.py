from odoo import models, fields

class AssetAsset(models.Model):
    _name = 'asset.asset'
    _description = 'Shared Asset'

    name = fields.Char(required=True)
    code = fields.Char()
    type = fields.Selection([
        ('device', 'Thiết bị'),
        ('vehicle', 'Phương tiện'),
        ('room', 'Phòng'),
        ('other', 'Khác')
    ], default='device')

    status = fields.Selection([
        ('available', 'Sẵn sàng'),
        ('using', 'Đang sử dụng'),
        ('maintenance', 'Bảo trì')
    ], default='available')

    description = fields.Text()
