from odoo import api, fields, models
import logging
import re

_logger = logging.getLogger(__name__)

ACCOUNT_REGEX = re.compile(r'(?:(\S*\d+\S*))?(.*)')
ACCOUNT_CODE_REGEX = re.compile(r'^[A-Za-z0-9.]+$')

class NewsInformation(models.Model):
    _name = "newsinformation.newsinformation"
    _description = "News Management"

    title = fields.Char(string="Tiêu đề tin tức")
    content = fields.Text(string = "Nội dung tin tức")
    id_user = fields.Many2one("userinformation.userinformation",
        string="ID người dùng",
        required=False,
        ondelete="cascade",)
    id_new = fields.One2many("commentinformation.commentinformation",
        "new_id",
        string="ID bài viết",
        required=True,
        ondelete="cascade",)
    id_category = fields.Many2one("categoriesinformation.categoriesinformation",
        string="Tên danh mục",
        required=True,
        ondelete="cascade",)
    url_image = fields.Text(string = "URL Hình ảnh tin tức")
    createtime = fields.Datetime(string = "Ngày xuất bản tin tức")

    comment_count = fields.Integer(string="Số lượng bình luận", compute="_compute_comment_count")

    @api.depends('id_new')
    def _compute_comment_count(self):
        for record in self:
            # print(f"Comments linked to article {record.id}: {record.id_new.ids}")
            record.comment_count = len(record.id_new)

