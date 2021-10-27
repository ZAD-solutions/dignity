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


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    age_group_id = fields.Many2one(comodel_name='age.groups', string='Age Group',
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
    degree_ids = fields.One2many(comodel_name='res.partner.degree', inverse_name='partner_id', )
    is_gezira_member = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                        string='Are you a Member Of Gezira Club ?', )
    is_heliopolis_member = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                            string='Are you a Member Of Heliopolis Club ?', )
    favourite_pastime = fields.Char(string='Favourite Pastime')
    favourite_pastime_ids = fields.Many2many(comodel_name='pastime', string='Favourite Pastime')
    campaign_id = fields.Many2one('utm.campaign', 'Campaign', )
    source_id = fields.Many2one('utm.source', 'Source', )
    medium_id = fields.Many2one('utm.medium', 'Medium', )
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
                                        string='Prefer Which type of food?', )
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
    # favourite_source_of_protein = fields.Char('Favourite source of Protein')
    favourite_source_of_protein = fields.Many2many('favourite.source.of.protein', string='Favourite source of Protein')
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
                                   string='Driver Type', )
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

    what_do_you_enjoy_the_most = fields.Many2many(comodel_name='enjoy.most', string='What do you enjoy the most?', )
    favourite_format_of_art = fields.Many2many(comodel_name='favourite.format.of.art',
                                               string='Favourite Format of Art?')
    type_of_musician = fields.Selection([('old', 'Old'), ('new', 'New')], string='Type of Musician', )
    favourite_music = fields.Many2many(comodel_name='favourite.music', string='Favourite Music', )
    which_music_will_elevate_your_mode = fields.Char('Which Music will Elevate your Mode?')
    favourite_genre_of_movies = fields.Many2many(comodel_name='favourite.genre.of.movies',
                                                 string='Favourite Genre of Music?', )
    what_sports_club_are_you_member_in = fields.Char(string='Which sports club are you member in?')
    favourite_cuisines = fields.Many2many(comodel_name='favourite.cuisines', string='What are your Favourite Cuisines')
    favourite_sport_to_engage = fields.Many2many(comodel_name='favourite.sport.to.engage',
                                                 string='Favorite sport to engage ?')
    favourite_sport_to_watch = fields.Many2many(comodel_name='favourite.sport.to.watch',
                                                string='Favorite sport to watch ?')
    board_games = fields.Many2many(comodel_name='board.games', string='Board Games')
    football_club = fields.Many2many(comodel_name='football.club', string='Football Club')
    team_type = fields.Selection([('team_based', 'Team Based'), ('solo_based', 'Solo Based')], string='Team Type')
    good_mode_while_dinning = fields.Many2many(comodel_name='good.mode.dinning',
                                               string='What view will put you in a good mode while dinning ?')
    favourite_local_destination = fields.Many2many(comodel_name='favourite.local.destination',
                                                   string='Favorite local destination/s')
    other_destination_info = fields.Char('Other Info')
    city_or_beach = fields.Selection([('city', 'City'), ('beach', 'Beach')], string='City or Beach?')
    preferred_season = fields.Many2many(comodel_name='preferred.season', string='Preferred Season')
    sun_or_shade = fields.Selection([('sun', 'Sun'), ('shade', 'Shade')], string='Do you enjoy the sun or shade ?')
    arrangement_of_your_dream_vacation = fields.Char('What might be the arrangement of your dream vacation?')
    like_to_dine = fields.Many2many(comodel_name='like.to.dine', string='Where do you like to dine?')
    shopping_or_delivery = fields.Selection([('shopping', 'Shopping'), ('delivery', 'Delivery')],
                                            string='Prefer Shopping or delivery?')
    preferred_chocolate = fields.Many2many(comodel_name='preferred.chocolate', string='Preferred chocolate')
    love_pets = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Do you have a pet?')
    pet_info = fields.Char("Pet Info")
    grow_plants = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Do you grow plants in your home?')
    enjoy_reading = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Do you enjoy reading?')
    which_book_category = fields.Char('Which Book Category')
    favourite_color = fields.Char('Favourite Color')
    make_up_do_you_use = fields.Char('What make up do you usually use?')

    might_annoy_you = fields.Char('What is the most thing that might annoy you while having lunch at a restaurant?')
    bad_mode_while_eating = fields.Char('What will put you in a bad mood while eating?')
    looking_for_restaurant_menu = fields.Char('What are you looking for in restaurant menu?')
    annoying_in_hotel_rooms = fields.Char('What you usually find annoying in hotel rooms?')
    compound_community_space = fields.Char('If you live in compound , what are you currently missing in your compound '
                                           ', or what do you want to solve in your community space ?')
    hate_from_start_to_arrive = fields.Char('If you are driving, what is the most think you hate from start to arrive?')
    make_your_life_easier = fields.Char('What do you think you need to change in your bathroom that may make your life easier?')
    living_room_more_convenient = fields.Char('What changes you may need to make your living room more convenient?')
    kitchen_more_convenient = fields.Char('What changes you may need to make your Kitchen more convenient?')
    surroundings = fields.Char('What is your main general problem that you always think about it in your surroundings?')
    going_shopping_in_mall = fields.Char('What is the main thing that can stop you from going shopping in a mall?')
    invite_people_to_home_dinner = fields.Char('What is the main thing that can stop you from inviting people to a home dinner?')
    visiting_friend = fields.Char('What is the main problem that may stop you from visiting a friend?')
    annoying_in_clothing_store = fields.Char('What most annoys you in a clothes Store?')
    fitting_rooms_in_shops = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                              string='Do you find it easy to use the fitting rooms in shops?')

    is_vendor_only = fields.Boolean("Is a Vendor Only")
    is_parent = fields.Boolean()
    is_child = fields.Boolean()
    is_main_contact = fields.Boolean()
    main_contact = fields.Char(compute='_get_main_contact')
    is_other_local_destination = fields.Boolean(compute='_compute_is_other_local_destination')
    lead_id = fields.Many2one('crm.lead')

    @api.onchange('favourite_local_destination')
    def _compute_is_other_local_destination(self):
        for record in self:
            record.is_other_local_destination = False
            if record.favourite_local_destination:
                for line in record.favourite_local_destination:
                    if line.name == 'Other':
                        record.is_other_local_destination = True

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
            # if self.country_id.id == 65:
            # if self.mobile and not re.match("^\d{11}$", self.mobile):
            #     raise UserError('Please enter 11 digits for the mobile number (%s).' % self.mobile)
