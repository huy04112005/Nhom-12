from odoo import models, fields

class MeetingRoom(models.Model):
    _name = 'meeting.room'
    _description = 'Meeting Room'

    name = fields.Char(required=True)
    location = fields.Char()
    capacity = fields.Integer()
    status = fields.Selection([
        ('available', 'Trống'),
        ('busy', 'Đang dùng'),
        ('maintenance', 'Bảo trì')
    ], default='available')

    description = fields.Text()
