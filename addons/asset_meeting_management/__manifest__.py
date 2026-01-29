{
    'name': 'Asset & Meeting Room Management',
    'version': '1.0',
    'summary': 'Quản lý tài sản và phòng họp dùng chung',
    'category': 'Administration',
    'author': 'Internship Project',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/asset_views.xml',
        'views/meeting_room_views.xml',
        'views/booking_views.xml',
    ],
    'installable': True,
    'application': True,
}
