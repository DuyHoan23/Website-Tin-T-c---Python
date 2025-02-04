from odoo import api, fields, models
import logging
import re

_logger = logging.getLogger(__name__)

ACCOUNT_REGEX = re.compile(r'(?:(\S*\d+\S*))?(.*)')
ACCOUNT_CODE_REGEX = re.compile(r'^[A-Za-z0-9.]+$')

class UserInfor(models.Model):
    _name = "userinformation.userinformation"
    _description = "User Management"



    userName = fields.Char(string="Tên người dùng")
    email = fields.Char(string="Email")
    password = fields.Char(string="Mật khẩu")
    url_img = fields.Text(string="Url hình ảnh")
    id_user = fields.One2many("commentinformation.commentinformation",
        "id",
        string="ID người dùng",
        required=False,
        ondelete="cascade",)
    # preferences = fields.Text(string="Preferences")
    # readingHistory = fields.Text(string="Lịch sử đọc sách")

    def check_password(self, password):
        return password == self.password


    def print_user_report(self):
        return self.env.ref('news.action_report_user').report_action(self)

    def print_all_user_report(self):
        # Lấy tất cả các bản ghi từ model userinformation.userinformation
        records = self.env['userinformation.userinformation'].search([])

        # Truyền tất cả các bản ghi vào báo cáo
        return self.env.ref('news.action_report_user_all').report_action(records)