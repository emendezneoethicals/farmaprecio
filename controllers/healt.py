from odoo import http
from odoo.http import request

class HealthPlanController(http.Controller):

    @http.route('/planes', type='http', auth='public', website=True)
    def view_health_plans(self, **kwargs):
        health_plans = request.env['health.plan'].sudo().search([])
        return request.render('farmaprecio.health_plans_page', {
            'health_plans': health_plans
        })

    @http.route('/planes/<int:plan_id>', type='http', auth='public', website=True)
    def view_health_plan_details(self, plan_id, **kwargs):
        plan = request.env['health.plan'].sudo().browse(plan_id)
        if not plan.exists():
            return request.not_found() 
        return request.render('farmaprecio.health_plan_detail', {
            'plan': plan
        })