# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    app_author_ids = fields.Many2many(
        string='Authors', comodel_name='odoo.author',
        relation='product_template_author_rel',
        column1='product_tmpl_id',
        column2='author_id',
        multi='author',
        compute="_compute_app_author_ids",
        store=True,)

    @api.depends('product_variant_ids', 'product_variant_id',
                 'product_variant_ids.app_author_ids',
                 'product_variant_id.app_author_ids')
    def _compute_app_author_ids(self):
        for template in self:
            author_ids = template.get_author_details()
            app_author_ids = self.env['odoo.author']
            for author in author_ids:
                app_author_ids += author
            template.app_author_ids = app_author_ids

    def get_author_details(self):
        author_ids = []
        for variant in self.product_variant_ids:
            for author in variant.app_author_ids:
                if author not in author_ids:
                    author_ids.append(author)
        return author_ids

    def get_version_info(self):
        products = self.product_variant_ids.sorted(
            lambda a: a.attribute_value_ids.sequence,  reverse=True)
        return products[0]
