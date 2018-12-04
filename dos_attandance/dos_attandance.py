from openerp import models, fields, api
from datetime import datetime, timedelta
class dos_attandance(models.Model):
    _inherit='hr_timesheet_sheet.sheet'
    dos_period_ids = fields.One2many('dos_attandance_tree','dos_period_id','Dos Period IDS')
    dates = []
    @api.multi
    def action_create_check_list(self):
        self.env['dos_attandance_tree'].search([]).unlink()
        if len(self.attendances_ids) > len(self.dos_period_ids)*2:
            self.dos_period_ids = self._prepare_check_list_lines()
        self.env.cr.execute("SELECT name, SUM(attendance) as total_attendance,total_timesheet FROM dos_attandance_tree GROUP BY name,total_timesheet ORDER BY name ASC")
        res_signout = self.env.cr.fetchall()
        self.env['dos_attandance_tree'].search([]).unlink()
        if len(self.attendances_ids) > len(self.dos_period_ids)*2:
            self.dos_period_ids = self._prepare_update_data_list_line(res_signout)
        return True
    @api.multi
    def _prepare_check_list_lines(self):
        new_data = []
        for line in self.attendances_ids:
            if line.action == 'sign_out':
                
                self.env.cr.execute("SELECT name FROM hr_attendance WHERE employee_id = "+str(line.employee_id.id) +" AND name < '"+str(line.name)+"' AND action = 'sign_in'  ORDER BY name DESC LIMIT 1")
                last_signin_id = self.env.cr.fetchall()
                info_one = tuple(last_signin_id[0])
                datefieldee = datetime.strptime(str(info_one[0]),  "%Y-%m-%d %H:%M:%S").date()
                
                print datefieldee
                data = self._prepare_check_list_line(line,datefieldee)
                new_data.append(data)
        return new_data
    @api.multi
    def _prepare_check_list_line(self, data,dateee):
        if self.attendances_ids:

            datefield = data.name
            #convert that str to strptime
            datefield1 = datetime.strptime(datefield,  "%Y-%m-%d %H:%M:%S")
            datefield2 = datetime.strptime(datefield,  "%Y-%m-%d %H:%M:%S").date()
            # add hours to converted time
            datefield1 = datefield1 - timedelta(hours=data.worked_hours)
            res = self.env['account.analytic.line'].search([('date','=',datefield2),('user_id','=',self.employee_id.user_id.id)])
            if(len(res) >= 2):
                total_time = 0
                for i  in res:
                    total_time = total_time + i.unit_amount
                print total_time
                difference = total_time - data.worked_hours    
            else:
                total_time = res.unit_amount
                difference = res.unit_amount - data.worked_hours
            
            #difference = res.unit_amount - data.worked_hours
            data = {
            'name': dateee,
            'attendance': data.worked_hours,
            'total_timesheet': total_time,
            'difference': difference,
            'action': data.action,
            }
     
            return data      

    @api.multi
    def _prepare_update_data_list_line(self, res_signout):
        if res_signout:
            new_data = []
            for result in res_signout:
                difference = result[1]- result[2]
                data = {
                'name': result[0],
                'attendance': result[1],
                'total_timesheet': result[2],
                'difference': difference,
                'action':'Sign Out',
                }
                new_data.append(data)
            return new_data 




class dos_attandance_tree(models.Model):
    _name='dos_attandance_tree'
    name = fields.Date('Date')
    attendance = fields.Float('Attendance')
    total_timesheet = fields.Float('Total Timesheet')
    difference = fields.Float('Difference')
    action = fields.Char('Action')
    dos_period_id = fields.Many2one('hr_timesheet_sheet.sheet','Dos Period Id')


class dos_attandance_hr(models.Model):
    _inherit='hr.attendance'
    @api.model
    def create(self, values):
        attendance_lines = self.env['dos_attandance_tree'].create(values)
        attendance_lines1 = self.env['dos_attandance_tree'].search([])
        result = super(dos_attandance_hr, self).create(values)

        return result
    