from email.policy import default

from dateutil.utils import today

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name='todo.task'
    _description = 'a model for daily tasks'


    name = fields.Char(string='Task Name', required=True)
    seq = fields.Char(default="New", readonly=True)
    active = fields.Boolean(default=True)
    assign_to = fields.Many2one('res.users')
    description = fields.Text()
    due_date = fields.Date(required=True)
    estimated_time = fields.Integer(required=True)
    is_late = fields.Boolean(default=False)
    employee_id = fields.Many2one('employee')
    assigned_tasks_id = fields.Many2many('assigned.tasks')
    status = fields.Selection([
        ('new','New'),
        ('in progress','In Progress'),
        ('completed','Completed'),
        ('closed','Closed'),
    ],default='new')
    todo_lines_ids = fields.One2many('todo.lines','task_id')

    def action_New(self):
        for rec in self:
            rec.status = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.status = 'in progress'

    def action_completed(self):
        for rec in self:
            rec.status = 'completed'

    def action_closed(self):
        for rec in self:
            rec.status = 'closed'
            # rec.active = False

    @api.constrains('estimated_time','todo_lines_ids')
    def check_estimated_times(self):
        for rec in self:
            total_times = 0
            for each_rec in rec.todo_lines_ids:
                total_times += each_rec.time_taken
            if rec.estimated_time < total_times:
                raise ValidationError('Ur estimated time less than total time ')

    def checking_due_date_is_late(self):
        task_ids = self.search([])
        today_date = fields.Date.today()

        for rec in task_ids:
            if rec.due_date <= today_date:
                rec.is_late = True
            else:
                rec.is_late = False
    @api.model
    def create(self, vals):
        res = super(TodoTask, self).create(vals)
        res.seq = self.env['ir.sequence'].next_by_code('task_sequence')
        res.assign_to = self.env.uid
        return res

    def open_assign_to_wizard(self):
        status = []
        for rec in self:
            status.append(rec.status)
            forbidden_status = ['closed','sold']
            if set(status).intersection(forbidden_status):
                raise ValidationError("You can't assign these records")
            else:
                action = self.env['ir.actions.actions']._for_xml_id('todo_managment.user_view_wizard_action')
                ids = []
                for rec in self:
                    ids.append(rec.id)
                action['context'] = {'default_task_ids': ids}
                return action


class TodoLines(models.Model):
    _name='todo.lines'
    _description = 'Times for each task'


    date = fields.Date(default=fields.Date.today() ,readonly=True)
    time_taken = fields.Integer()
    description = fields.Text()
    task_id = fields.Many2one('todo.task',readonly=True)