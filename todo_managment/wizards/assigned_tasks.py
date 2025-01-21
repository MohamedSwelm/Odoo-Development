from email.policy import default

from odoo import fields, models

class AssignedTasks(models.TransientModel):
    _name='assigned.tasks'

    assign_to =fields.Many2one('employee')
    task_ids = fields.Many2many('todo.task')



    def action_confirm(self):
        employee_model = self.env['employee']
        employee_id= employee_model.search([('name','=',self.assign_to.name)])
        print(employee_id)
        print(employee_id.name)
        employee_id.write({
            "task_ids":self.task_ids
        })

        # for task in all_tasks:
        #     task.assign_to =self.assign_to
