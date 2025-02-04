from odoo import api, fields, models
import logging
import re

from odoo.addons.test_impex.models import field

_logger = logging.getLogger(__name__)

ACCOUNT_REGEX = re.compile(r'(?:(\S*\d+\S*))?(.*)')
ACCOUNT_CODE_REGEX = re.compile(r'^[A-Za-z0-9.]+$')

class CategoriesInformation(models.Model):
    _name = "categoriesinformation.categoriesinformation"
    _description = "News Management"
    _rec_name = "cate_name"
    id_cate = fields.One2many("newsinformation.newsinformation",
        "id",
        string="ID danh mục",
        required=True,
        ondelete="cascade",)
    cate_name = fields.Char(string = "Tên danh mục")

