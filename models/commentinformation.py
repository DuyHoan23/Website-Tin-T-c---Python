import self

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class CommentInformation(models.Model):
    _name = "commentinformation.commentinformation"
    _description = "Comment Management"

    new_id = fields.Many2one(
        "newsinformation.newsinformation",
        string="ID tin tức",
        required=True,
        ondelete="cascade",
    )
    user_id = fields.Many2one(
        "userinformation.userinformation",
        string="ID người dùng",
        required=True,
        ondelete="cascade",
    )
    content = fields.Text(string="Nội dung bình luận")
    timestamps = fields.Datetime(string="Ngày giờ bình luận", default=fields.Datetime.now)
    state = fields.Selection(selection=[('Đã duyệt','Đã duyệt'),
                                        ('Chưa duyệt','Chưa duyệt')], string='State', default='Chưa duyệt')


    def set_cmt_through(self):
        for cmt in self:
            cmt.state = 'Đã duyệt'

    def set_cmt_not_through(self):
        for cmt in self:
            cmt.state = 'Chưa duyệt'