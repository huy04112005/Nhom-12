from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AssetBooking(models.Model):
    _name = 'asset.booking'
    _description = 'Asset & Room Booking'
    _rec_name = 'purpose' # Để khi tìm kiếm sẽ hiện tên theo Mục đích

    # --- Khai báo các trường dữ liệu (Fields) ---
    asset_id = fields.Many2one('asset.asset', string='Tài sản')
    room_id = fields.Many2one('meeting.room', string='Phòng họp')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, string='Người đặt')
    
    start_time = fields.Datetime(string='Bắt đầu', required=True)
    end_time = fields.Datetime(string='Kết thúc', required=True)
    purpose = fields.Char(string='Mục đích', required=True)
    
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('approved', 'Đã duyệt'),
        ('done', 'Hoàn thành'),
        ('cancel', 'Hủy')
    ], default='draft', string='Trạng thái')

    # --- Logic chặn trùng lịch (Đã sửa lỗi logic) ---
    @api.constrains('start_time', 'end_time', 'asset_id', 'room_id')
    def _check_conflict(self):
        for rec in self:
            # 1. Kiểm tra logic thời gian cơ bản
            if rec.start_time >= rec.end_time:
                raise ValidationError("Thời gian Kết thúc phải sau thời gian Bắt đầu!")

            # 2. Định nghĩa điều kiện tìm kiếm các đơn ĐÃ DUYỆT và bị TRÙNG GIỜ
            # Logic: (StartA < EndB) và (EndA > StartB) là công thức tìm giao nhau
            base_domain = [
                ('id', '!=', rec.id),              # Không tính chính đơn này
                ('state', 'in', ['approved']),     # Chỉ check các đơn đã duyệt (đơn Nháp/Hủy không tính)
                ('start_time', '<', rec.end_time), 
                ('end_time', '>', rec.start_time)
            ]

            # 3. Kiểm tra riêng: Trùng PHÒNG
            if rec.room_id:
                # Tạo domain mới kết hợp base_domain + điều kiện phòng
                room_domain = base_domain + [('room_id', '=', rec.room_id.id)]
                if self.search_count(room_domain) > 0:
                    raise ValidationError(f"❌ Phòng '{rec.room_id.name}' đã có người đặt trong khung giờ này!")

            # 4. Kiểm tra riêng: Trùng TÀI SẢN
            if rec.asset_id:
                # Tạo domain mới kết hợp base_domain + điều kiện tài sản
                asset_domain = base_domain + [('asset_id', '=', rec.asset_id.id)]
                if self.search_count(asset_domain) > 0:
                    raise ValidationError(f"❌ Tài sản '{rec.asset_id.name}' đang bận trong khung giờ này!")

    # --- Các hàm xử lý nút bấm (Workflow Actions) ---
    def action_approve(self):
        # Có thể thêm logic: Chỉ Admin mới được duyệt
        self._check_conflict() # Check lại lần nữa trước khi duyệt cho chắc
        self.state = 'approved'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'
    def action_approve(self):
        # 1. Kiểm tra logic trùng lặp
        self._check_conflict()
        
        # 2. Đổi trạng thái đơn đặt
        self.state = 'approved'
        
        # 3. [TỰ ĐỘNG HÓA - MỨC 2] 
        # Tự động cập nhật trạng thái Tài sản sang 'Đang sử dụng' (using)
        if self.asset_id:
            self.asset_id.status = 'using'
            
    def action_done(self):
        self.state = 'done'
        # [TỰ ĐỘNG HÓA - MỨC 2]
        # Khi hoàn thành, tự động trả tài sản về trạng thái 'Sẵn sàng'
        if self.asset_id:
            self.asset_id.status = 'available'