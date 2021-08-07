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
                   ('5', '5'), ]


class CRMLeadInherit(models.Model):
    _inherit = 'crm.lead'

    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True, )
    age_group_id = fields.Many2one(comodel_name='age.groups', required='True', string='Age Group',
                                   track_visibility='onchange', )
    birthdate = fields.Date('Birth Date', )
    age = fields.Char(compute="get_partner_age", string='Age', store=True, )
    marital_status = fields.Selection([('single', 'Single'),
                                       ('married', 'Married'),
                                       ('divorced', 'Divorced'),
                                       ('separated', 'Separated'),
                                       ], string='Marital Status', )
    children_no = fields.Integer(string='No. of Children', )
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    # household_income = fields.Monetary(string='Household Income', currency_field="currency_id", )
    degree_ids = fields.One2many(comodel_name='res.partner.degree', inverse_name='lead_id', )
    is_gezira_member = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                        string='Are you a Member Of Gezira Club ?', )
    is_heliopolis_member = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                            string='Are you a Member Of Heliopolis Club ?', )
    favourite_pastime = fields.Char(string='Favourite Pastime')
    favourite_pastime_ids = fields.Many2many(comodel_name='pastime', string='Favourite Pastime')
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
    # drinking_alcohol = fields.Selection([('yes', 'Yes'), ('no', 'No')],
    #                                     string='Drinking Alcohol ?', )
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
    medical_issues_ids = fields.One2many(comodel_name='medical.issues', inverse_name='lead_id', )
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

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        res = super(CRMLeadInherit, self)._prepare_customer_values(partner_name, is_company=False, parent_id=False)
        res['gender'] = self.gender
        res['age_group_id'] = self.age_group_id.id
        res['birthdate'] = self.birthdate
        res['age'] = self.age
        res['marital_status'] = self.marital_status
        res['children_no'] = self.children_no
        res['currency_id'] = self.currency_id
        # res['household_income'] = self.household_income
        res['is_gezira_member'] = self.is_gezira_member
        res['is_heliopolis_member'] = self.is_heliopolis_member
        res['favourite_pastime'] = self.favourite_pastime
        res['favourite_pastime_ids'] = self.favourite_pastime_ids.ids
        res['campaign_id'] = self.campaign_id.id
        res['source_id'] = self.source_id.id
        res['medium_id'] = self.medium_id.id
        res['referred'] = self.referred
        res['need_assist'] = self.need_assist
        res['socialize_member'] = self.socialize_member
        res['on_diet'] = self.on_diet
        res['diet_type'] = self.diet_type
        res['any_restrictions'] = self.any_restrictions
        res['more_info'] = self.more_info
        res['fruits_or_sweets'] = self.fruits_or_sweets
        res['weight_goals'] = self.weight_goals
        res['homemade_or_fast_food'] = self.homemade_or_fast_food
        res['meals_per_day'] = self.meals_per_day
        res['salty_or_non_salty'] = self.salty_or_non_salty
        res['water_per_day'] = self.water_per_day
        # res['drinking_alcohol'] = self.drinking_alcohol
        res['favourite_breakfast'] = self.favourite_breakfast
        res['favourite_lunch'] = self.favourite_lunch
        res['favourite_dinner'] = self.favourite_dinner
        res['favourite_source_of_protein'] = self.favourite_source_of_protein
        res['vitamin_d'] = self.vitamin_d
        res['time_in_sun'] = self.time_in_sun
        res['healthy_level'] = self.healthy_level
        res['missing_from_diet'] = self.missing_from_diet
        res['chronic_diseases'] = self.chronic_diseases
        res['chronic_diseases_ids'] = self.chronic_diseases_ids.ids
        res['medication'] = self.medication
        res['medical_issues'] = self.medical_issues
        res['injuries'] = self.injuries
        res['serious_or_permanent_injuries'] = self.serious_or_permanent_injuries
        res['activity_level'] = self.activity_level
        res['disabilities_or_handicaps'] = self.disabilities_or_handicaps
        res['disability_type_ids'] = self.disability_type_ids.ids
        res['any_past_emotional_trauma'] = self.any_past_emotional_trauma
        res['emotional_trauma'] = self.emotional_trauma
        res['favourite_actor'] = self.favourite_actor
        res['favourite_actress'] = self.favourite_actress
        res['favourite_egyptian_movie'] = self.favourite_egyptian_movie
        res['favourite_tv_show'] = self.favourite_tv_show
        res['favourite_international_movie'] = self.favourite_international_movie
        res['favourite_musician'] = self.favourite_musician
        res['do_you_read'] = self.do_you_read
        res['favourite_book'] = self.favourite_book
        res['favourite_writer'] = self.favourite_writer
        res['do_you_play_music'] = self.do_you_play_music
        res['do_you_play_sports'] = self.do_you_play_sports
        res['favourite_board_game'] = self.favourite_board_game
        res['team_type'] = self.team_type
        res['preferred_holidays'] = self.preferred_holidays
        res['preferred_destination'] = self.preferred_destination.ids
        res['other_destination'] = self.other_destination
        res['own_or_rent'] = self.own_or_rent
        res['summer_or_winter'] = self.summer_or_winter
        res['remote_destination'] = self.remote_destination
        res['go_out_cairo'] = self.go_out_cairo
        res['own_car'] = self.own_car
        res['do_you_drive'] = self.do_you_drive
        res['do_you_have_driver'] = self.do_you_have_driver
        res['uber_or_family'] = self.uber_or_family
        res['use_subscription'] = self.use_subscription
        res['subscription_date'] = self.subscription_date
        res['discontinued'] = self.discontinued
        res['discontinued_reason_ids'] = self.discontinued_reason_ids.ids
        res['social_follower'] = self.social_follower
        res['social_media_ids'] = self.social_media_ids.ids
        res['recommended_products_and_services'] = self.recommended_products_and_services
        return res

    def _create_customer(self):
        """ Create a partner from lead data and link it to the lead.

        :return: newly-created partner browse record
        """
        Partner = self.env['res.partner']
        contact_name = self.contact_name
        if not contact_name:
            contact_name = Partner._parse_partner_name(self.email_from)[0] if self.email_from else False

        if self.partner_name:
            print('1111111111111111111')
            partner_company = Partner.create(self._prepare_customer_values(self.partner_name, is_company=True))
            # Prepare one2many fields
            degree_lines = []
            medical_issues = []
            for line in self.degree_ids:
                degree_lines.append({
                    'degree_id': line.degree_id.id,
                    'institutions_id': line.institutions_id.id,
                    'date': line.date,
                    'partner_id': partner_company.id,
                })
            for line in self.medical_issues_ids:
                medical_issues.append({
                    'type': line.type,
                    'date': line.date,
                    'more_info': line.more_info,
                    'partner_id': partner_company.id,
                })
            partner_company.write({'degree_ids': [(0, 0, line) for line in degree_lines]})
            partner_company.write({'medical_issues_ids': [(0, 0, line) for line in medical_issues]})
            # END
        elif self.partner_id:
            partner_company = self.partner_id
        else:
            partner_company = None

        if contact_name:
            print('222222222222222222')
            new_partner = Partner.create(self._prepare_customer_values(contact_name, is_company=False,
                                                         parent_id=partner_company.id if partner_company else False))
            # Prepare one2many fields
            degree_lines = []
            medical_issues = []
            for line in self.degree_ids:
                degree_lines.append({
                    'degree_id': line.degree_id.id,
                    'institutions_id': line.institutions_id.id,
                    'date': line.date,
                    'partner_id': new_partner.id,
                })
            for line in self.medical_issues_ids:
                medical_issues.append({
                    'type': line.type,
                    'date': line.date,
                    'more_info': line.more_info,
                    'partner_id': new_partner.id,
                })
            new_partner.write({'degree_ids': [(0, 0, line) for line in degree_lines]})
            new_partner.write({'medical_issues_ids': [(0, 0, line) for line in medical_issues]})
            # END
            return new_partner

        if partner_company:
            return partner_company
        new_partner_id = Partner.create(self._prepare_customer_values(self.name, is_company=False))
        # Prepare one2many fields
        degree_lines = []
        medical_issues = []
        for line in self.degree_ids:
            degree_lines.append({
                'degree_id': line.degree_id.id,
                'institutions_id': line.institutions_id.id,
                'date': line.date,
                'partner_id': new_partner_id.id,
            })
        for line in self.medical_issues_ids:
            medical_issues.append({
                'type': line.type,
                'date': line.date,
                'more_info': line.more_info,
                'partner_id': new_partner_id.id,
            })
        new_partner_id.write({'degree_ids': [(0, 0, line) for line in degree_lines]})
        new_partner_id.write({'medical_issues_ids': [(0, 0, line) for line in medical_issues]})
        # END
        return new_partner_id