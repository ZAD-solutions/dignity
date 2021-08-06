# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re
from dateutil.relativedelta import relativedelta
NUMBER_SELECTIONS = [('1', '1'),
                     ('2', '2'),
                     ('3', '3'),
                     ('4', '4'),
                     ('5', '5'),
                     ('6', '6'),
                     ('7', '7'),
                     ('8', '8'),
                     ('9', '9'),
                     ('10', '10')]
FIVE_SELECTIONS = [('1', '1'),
                   ('2', '2'),
                   ('3', '3'),
                   ('4', '4'),
                   ('5', '5'),]


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True, )
    age_group_id = fields.Many2one(comodel_name='age.groups', required='True', string='Age Group',
                                   track_visibility='onchange', )
    birthdate = fields.Date('Birth Date', )
    age = fields.Char(compute="get_partner_age", string='Age', store=True,)
    marital_status = fields.Selection([('single', 'Single'),
                                       ('married', 'Married'),
                                       ('divorced', 'Divorced'),
                                       ('separated', 'Separated'),
                                       ], string='Marital Status', )
    children_no = fields.Integer(string='No. of Children',)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    household_income = fields.Monetary(string='Household Income', currency_field="currency_id", )
    degree_ids = fields.One2many(comodel_name='res.partner.degree', inverse_name='partner_id', )
    is_gezira_member = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                        string='Are you a Member Of Gezira Club ?', )
    is_heliopolis_member = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                            string='Are you a Member Of Heliopolis Club ?', )
    favourite_pastime = fields.Char(string='Favourite Pastime')
    favourite_pastime_ids = fields.Many2many(comodel_name='pastime', string='Favourite Pastime')
    campaign_id = fields.Many2one('utm.campaign', 'Campaign',)
    source_id = fields.Many2one('utm.source', 'Source',)
    medium_id = fields.Many2one('utm.medium', 'Medium',)
    referred = fields.Char('Referred By')
    need_assist = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                   string='Would you like Our Team to stay nearby to physically assist you ?', )
    socialize_member = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                        string='Do you socialize with member ?', )
    on_diet = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                               string='Are You on a Diet ?', )
    diet_type = fields.Selection([('medical', 'Medical'),
                                  ('self', 'Self'),
                                  ('administered', 'Administered')],
                                 string='Diet Type', )
    any_restrictions = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                        string='Any Restrictions or Allergies ?', )
    more_info = fields.Char('More Info')
    fruits_or_sweets = fields.Selection([('fruits', 'Fruits'),
                                         ('sweets', 'Sweets')],
                                        string='Prefer Fruits or Sweets as a source of Sugar', )
    weight_goals = fields.Char('Weight Goals if there', )
    homemade_or_fast_food = fields.Selection([('homemade', 'Homemade'),
                                              ('fast', 'Fast')],
                                             string='Prefer Fruits or Sweets as a source of Sugar', )
    meals_per_day = fields.Integer('How many meals per day')
    salty_or_non_salty = fields.Selection([('salty', 'Salty'),
                                           ('non_salty', 'Non Salty')],
                                          string='Salty or Non Salty', )
    water_per_day = fields.Float('How much water do you drink per day')
    drinking_alcohol = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                        string='Drinking Alcohol ?', )
    favourite_breakfast = fields.Char('Favourite Breakfast')
    favourite_lunch = fields.Char('Favourite Lunch')
    favourite_dinner = fields.Char('Favourite Dinner')
    favourite_source_of_protein = fields.Char('Favourite source of Protein')
    vitamin_d = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                 string='Do you supplement Vitamin D', )
    time_in_sun = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                   string='Do you spend enough time in the sun', )
    healthy_level = fields.Selection(FIVE_SELECTIONS, 'Healthy Level')
    missing_from_diet = fields.Char('What is missing from Diet', )
    chronic_diseases = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                        string='Any chronic diseases', )
    chronic_diseases_ids = fields.Many2many('chronic.diseases', string="Diseases")
    medication = fields.Char('What Medication are you on ?', )
    medical_issues = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                      string='Any medical Issues/Allergies/Surgeries', )
    medical_issues_ids = fields.One2many(comodel_name='medical.issues', inverse_name='partner_id', )
    injuries = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                string='Any serious or permanent Injuries', )
    serious_or_permanent_injuries = fields.Char('Injuries', )
    activity_level = fields.Selection(FIVE_SELECTIONS, 'Activity Level')
    disabilities_or_handicaps = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                 string='Any disabilities/handicaps?', )
    disability_type_ids = fields.Many2many('disabilities', string='Disability Type')
    any_past_emotional_trauma = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                 string='Any Any past Emotional Trauma?', )
    emotional_trauma = fields.Char('Emotional Trauma')
    favourite_actor = fields.Char()
    favourite_actress = fields.Char()
    favourite_egyptian_movie = fields.Char()
    favourite_tv_show = fields.Char()
    favourite_international_movie = fields.Char()
    favourite_musician = fields.Char()
    do_you_read = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                   string='Do you read ?', )
    favourite_book = fields.Char()
    favourite_writer = fields.Char()
    do_you_play_music = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                         string='Do you play music ?', )
    do_you_play_sports = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                          string='Do you play Sports ?', )
    favourite_board_game = fields.Char()
    team_type = fields.Selection([('team_based', 'Team Based'), ('solo_activity', 'Solo Activity')],
                                 string='Team Type', )
    preferred_holidays = fields.Selection([('staying', 'Staying'), ('traveling', 'Traveling')],
                                          string='Preferred Holidays', )
    preferred_destination = fields.Many2many(comodel_name='preferred.destination', )
    other_destination = fields.Char()
    own_or_rent = fields.Selection([('own', 'Own'), ('rent', 'Rent')],
                                   string='Do you own or rent ?', )
    summer_or_winter = fields.Selection([('summer', 'Summer'), ('winter', 'Winter')],
                                        string='Prefer summer or winter ?', )
    remote_destination = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                          string='Would you visit a remote destination line Siwa/Fayum ?', )
    go_out_cairo = fields.Char('Where do you like to go out in Cairo ?', )
    own_car = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                               string='Do you own a Car ?', )
    do_you_drive = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                    string='Do you drive ?', )
    do_you_have_driver = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                          string='Have a driver ?', )
    driver_type = fields.Selection([('full_time', 'Full time driver'), ('car_giver', 'Car Giver')],
                                   string='Have a driver ?', )
    uber_or_family = fields.Selection([('uber', 'Uber'), ('family', 'Family')],
                                      string='Do you use Uber of Family ?', )
    use_subscription = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                        string='Use Subscription ?', )
    subscription_date = fields.Date('Subscription Date')
    discontinued = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                    string='Discontinued ?', )
    discontinued_reason_ids = fields.Many2many(comodel_name='subscription.discontinued.reasons',
                                               string='Subscription Discontinued Reasons', )
    social_follower = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                       string='Social Follower ?', )
    social_media_ids = fields.Many2many(comodel_name='social.media', string='Social Media', )
    recommended_products_and_services = fields.Selection(NUMBER_SELECTIONS,
                                                         string='How likely to recommend our products & services to '
                                                                'others')
    is_parent = fields.Boolean()
    is_child = fields.Boolean()
    is_main_contact = fields.Boolean()
    main_contact = fields.Char(compute='_get_main_contact')

    def _get_main_contact(self):
        for partner in self:
            contact = ''
            if partner.child_ids:
                for child in partner.child_ids:
                    if child.is_main_contact:
                        contact = child.name
            partner.main_contact = contact

    @api.depends('birthdate')
    def get_partner_age(self):
        for rec in self:
            age = ''
            if rec.birthdate:
                end_data = fields.Datetime.now()
                delta = relativedelta(end_data, rec.birthdate)
                age = str(delta.years) + _(" Year ") + str(delta.months) + _(" Month ") + str(delta.days) + _(
                        " Days")
            rec.age = age

    @api.constrains('mobile')
    def _check_mobile_uniqueness(self):
        if self.mobile:
            if self.search_count([('mobile', '=', self.mobile)]) > 1:
                raise UserError('Another Customer/Vendor already has this Mobile (%s)' % self.mobile)
            # if self.mobile and not self.mobile.isdigit():
            #     raise UserError('The Mobile (%s) Is Not Valid Format' % self.mobile)
            if self.country_id.id == 65:
                if self.mobile and not re.match("^\d{11}$", self.mobile):
                    raise UserError('Please enter 11 digits for the mobile number (%s).' % self.mobile)

    # Override these fields to ignore server core addons versions conflicts
    # stage_id = fields.Many2one(comodel_name='crm.stage')