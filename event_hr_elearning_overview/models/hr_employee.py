# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
 
    _description = 'scaffold_test.scaffold_test'
    _inherit="hr.employee" 

    def test(self):
        pass