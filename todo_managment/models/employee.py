from odoo import models, fields

class Employee(models.Model):
    _name = 'employee'
    _description = 'employee model'

    name = fields.Char(string= 'Employee Name')
    task_ids = fields.One2many('todo.task','employee_id')
    assign_to = fields.Many2one('todo.task')