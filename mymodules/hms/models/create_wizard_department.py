from odoo import models, fields

# reocrd is saved while preoforming actions and then deleted from the daatabase
class DepartmentWizard(models.TransientModel):
    _name='hms.departmentwizard'
    name=fields.Char()
    description=fields.Text()
    def save_department(self):
        # put inside .env the table name 
        # to create new department 
        self.env['hms.department'].create({

            'name': self.name,
            'capacity':self.capacity,
        })
        #####################################################################
        # to search
        students= self.env['hms.patient'].search([('state','=','good')])
        #########################################################################
        # to update use ("write")
        students.write({
            'state':'fair'
        })
        ####################################################################################
        # to delete use ("unlink")
        students.unlink()

        # to return the name of the search results
        # print(students.mapped('name'))