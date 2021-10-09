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
    make_your_life_easier = fields.Char(
        'What do you think you need to change in your bathroom that may make your life easier?')
    living_room_more_convenient = fields.Char('What changes you may need to make your living room more convenient?')
    kitchen_more_convenient = fields.Char('What changes you may need to make your Kitchen more convenient?')
    surroundings = fields.Char('What is your main general problem that you always think about it in your surroundings?')
    going_shopping_in_mall = fields.Char('What is the main thing that can stop you from going shopping in a mall?')
    invite_people_to_home_dinner = fields.Char(
        'What is the main thing that can stop you from inviting people to a home dinner?')
    visiting_friend = fields.Char('What is the main problem that may stop you from visiting a friend?')
    annoying_in_clothing_store = fields.Char('What most annoys you in a clothes Store?')
    fitting_rooms_in_shops = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                              string='Do you find it easy to use the fitting rooms in shops?')
    is_other_local_destination = fields.Boolean(compute='_compute_is_other_local_destination')

    @api.onchange('favourite_local_destination')
    def _compute_is_other_local_destination(self):
        for record in self:
            record.is_other_local_destination = False
            if record.favourite_local_destination:
                for line in record.favourite_local_destination:
                    if line.name == 'Other':
                        record.is_other_local_destination = True

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
        res['favourite_source_of_protein'] = self.favourite_source_of_protein.ids
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
        res['driver_type'] = self.driver_type
        res['uber_or_family'] = self.uber_or_family
        res['use_subscription'] = self.use_subscription
        res['subscription_date'] = self.subscription_date
        res['discontinued'] = self.discontinued
        res['discontinued_reason_ids'] = self.discontinued_reason_ids.ids
        res['social_follower'] = self.social_follower
        res['social_media_ids'] = self.social_media_ids.ids
        res['recommended_products_and_services'] = self.recommended_products_and_services
        res['what_do_you_enjoy_the_most'] = self.what_do_you_enjoy_the_most.ids
        res['favourite_format_of_art'] = self.favourite_format_of_art.ids
        res['type_of_musician'] = self.type_of_musician
        res['favourite_music'] = self.favourite_music.ids
        res['which_music_will_elevate_your_mode'] = self.which_music_will_elevate_your_mode
        res['favourite_genre_of_movies'] = self.favourite_genre_of_movies.ids
        res['what_sports_club_are_you_member_in'] = self.what_sports_club_are_you_member_in
        res['favourite_cuisines'] = self.favourite_cuisines.ids
        res['favourite_sport_to_engage'] = self.favourite_sport_to_engage.ids
        res['favourite_sport_to_watch'] = self.favourite_sport_to_watch.ids
        res['board_games'] = self.board_games.ids
        res['football_club'] = self.football_club.ids
        res['team_type'] = self.team_type
        res['good_mode_while_dinning'] = self.good_mode_while_dinning.ids
        res['favourite_local_destination'] = self.favourite_local_destination.ids
        res['other_destination_info'] = self.other_destination_info
        res['city_or_beach'] = self.city_or_beach
        res['preferred_season'] = self.preferred_season.ids
        res['sun_or_shade'] = self.sun_or_shade
        res['arrangement_of_your_dream_vacation'] = self.arrangement_of_your_dream_vacation
        res['like_to_dine'] = self.like_to_dine.ids
        res['shopping_or_delivery'] = self.shopping_or_delivery
        res['preferred_chocolate'] = self.preferred_chocolate.ids
        res['love_pets'] = self.love_pets
        res['pet_info'] = self.pet_info
        res['grow_plants'] = self.grow_plants
        res['enjoy_reading'] = self.enjoy_reading
        res['which_book_category'] = self.which_book_category
        res['favourite_color'] = self.favourite_color
        res['make_up_do_you_use'] = self.make_up_do_you_use
        res['might_annoy_you'] = self.might_annoy_you
        res['bad_mode_while_eating'] = self.bad_mode_while_eating
        res['looking_for_restaurant_menu'] = self.looking_for_restaurant_menu
        res['annoying_in_hotel_rooms'] = self.annoying_in_hotel_rooms
        res['compound_community_space'] = self.compound_community_space
        res['hate_from_start_to_arrive'] = self.hate_from_start_to_arrive
        res['make_your_life_easier'] = self.make_your_life_easier
        res['living_room_more_convenient'] = self.living_room_more_convenient
        res['kitchen_more_convenient'] = self.kitchen_more_convenient
        res['surroundings'] = self.surroundings
        res['going_shopping_in_mall'] = self.going_shopping_in_mall
        res['invite_people_to_home_dinner'] = self.invite_people_to_home_dinner
        res['visiting_friend'] = self.visiting_friend
        res['fitting_rooms_in_shops'] = self.fitting_rooms_in_shops
        res['is_other_local_destination'] = self.is_other_local_destination
        res['lead_id'] = self.id
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
                    # 'lead_id': self.id,
                })
            for line in self.medical_issues_ids:
                medical_issues.append({
                    'type': line.type,
                    'date': line.date,
                    'more_info': line.more_info,
                    'partner_id': partner_company.id,
                    # 'lead_id': self.id,
                })
            partner_company.write({'degree_ids': [(0, 0, line) for line in degree_lines]})
            partner_company.write({'medical_issues_ids': [(0, 0, line) for line in medical_issues]})
            # END
        elif self.partner_id:
            partner_company = self.partner_id
        else:
            partner_company = None

        if contact_name:
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
                    # 'lead_id': self.id,
                })
            for line in self.medical_issues_ids:
                medical_issues.append({
                    'type': line.type,
                    'date': line.date,
                    'more_info': line.more_info,
                    'partner_id': new_partner.id,
                    # 'lead_id': self.id,
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
                # 'lead_id': self.id,
            })
        for line in self.medical_issues_ids:
            medical_issues.append({
                'type': line.type,
                'date': line.date,
                'more_info': line.more_info,
                'partner_id': new_partner_id.id,
                # 'lead_id': self.id,
            })
        new_partner_id.write({'degree_ids': [(0, 0, line) for line in degree_lines]})
        new_partner_id.write({'medical_issues_ids': [(0, 0, line) for line in medical_issues]})
        # END
        return new_partner_id

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for record in self:
            if record.partner_id:
                record.gender = record.partner_id.gender
                record.age_group_id = record.partner_id.age_group_id.id if record.partner_id.age_group_id else False
                record.birthdate = record.partner_id.birthdate
                record.age = record.partner_id.age
                record.marital_status = record.partner_id.marital_status
                record.children_no = record.partner_id.children_no
                record.currency_id = record.partner_id.currency_id.id if record.partner_id.currency_id else False
                record.is_gezira_member = record.partner_id.is_gezira_member
                record.is_heliopolis_member = record.partner_id.is_heliopolis_member
                record.favourite_pastime = record.partner_id.favourite_pastime
                record.favourite_pastime_ids = record.partner_id.favourite_pastime_ids.ids
                record.campaign_id = record.partner_id.campaign_id.id if record.partner_id.campaign_id else False
                record.source_id = record.partner_id.source_id.id if record.partner_id.source_id else False
                record.medium_id = record.partner_id.medium_id.id if record.partner_id.medium_id else False
                record.referred = record.partner_id.referred
                record.need_assist = record.partner_id.need_assist
                record.socialize_member = record.partner_id.socialize_member
                record.on_diet = record.partner_id.on_diet
                record.diet_type = record.partner_id.diet_type
                record.any_restrictions = record.partner_id.any_restrictions
                record.more_info = record.partner_id.more_info
                record.fruits_or_sweets = record.partner_id.fruits_or_sweets
                record.weight_goals = record.partner_id.weight_goals
                record.homemade_or_fast_food = record.partner_id.homemade_or_fast_food
                record.meals_per_day = record.partner_id.meals_per_day
                record.salty_or_non_salty = record.partner_id.salty_or_non_salty
                record.water_per_day = record.partner_id.water_per_day
                record.favourite_breakfast = record.partner_id.favourite_breakfast
                record.favourite_lunch = record.partner_id.favourite_lunch
                record.favourite_dinner = record.partner_id.favourite_dinner
                record.favourite_source_of_protein = record.partner_id.favourite_source_of_protein.ids
                record.vitamin_d = record.partner_id.vitamin_d
                record.time_in_sun = record.partner_id.time_in_sun
                record.healthy_level = record.partner_id.healthy_level
                record.missing_from_diet = record.partner_id.missing_from_diet
                record.chronic_diseases = record.partner_id.chronic_diseases
                record.chronic_diseases_ids = record.partner_id.chronic_diseases_ids.ids
                record.medication = record.partner_id.medication
                record.medical_issues = record.partner_id.medical_issues
                record.injuries = record.partner_id.injuries
                record.serious_or_permanent_injuries = record.partner_id.serious_or_permanent_injuries
                record.activity_level = record.partner_id.activity_level
                record.disabilities_or_handicaps = record.partner_id.disabilities_or_handicaps
                record.disability_type_ids = record.partner_id.disability_type_ids.ids
                record.any_past_emotional_trauma = record.partner_id.any_past_emotional_trauma
                record.emotional_trauma = record.partner_id.emotional_trauma
                record.favourite_actor = record.partner_id.favourite_actor
                record.favourite_actress = record.partner_id.favourite_actress
                record.favourite_egyptian_movie = record.partner_id.favourite_egyptian_movie
                record.favourite_tv_show = record.partner_id.favourite_tv_show
                record.favourite_international_movie = record.partner_id.favourite_international_movie
                record.favourite_musician = record.partner_id.favourite_musician
                record.do_you_read = record.partner_id.do_you_read
                record.favourite_book = record.partner_id.favourite_book
                record.favourite_writer = record.partner_id.favourite_writer
                record.do_you_play_music = record.partner_id.do_you_play_music
                record.do_you_play_sports = record.partner_id.do_you_play_sports
                record.favourite_board_game = record.partner_id.favourite_board_game
                record.team_type = record.partner_id.team_type
                record.preferred_holidays = record.partner_id.preferred_holidays
                record.preferred_destination = record.partner_id.preferred_destination
                record.other_destination = record.partner_id.other_destination
                record.own_or_rent = record.partner_id.own_or_rent
                record.summer_or_winter = record.partner_id.summer_or_winter
                record.remote_destination = record.partner_id.remote_destination
                record.go_out_cairo = record.partner_id.go_out_cairo
                record.own_car = record.partner_id.own_car
                record.do_you_drive = record.partner_id.do_you_drive
                record.do_you_have_driver = record.partner_id.do_you_have_driver
                record.driver_type = record.partner_id.driver_type
                record.uber_or_family = record.partner_id.uber_or_family
                record.use_subscription = record.partner_id.use_subscription
                record.subscription_date = record.partner_id.subscription_date
                record.discontinued = record.partner_id.discontinued
                record.discontinued_reason_ids = record.partner_id.discontinued_reason_ids.ids
                record.social_follower = record.partner_id.social_follower
                record.social_media_ids = record.partner_id.social_media_ids.ids
                record.recommended_products_and_services = record.partner_id.recommended_products_and_services
                record.what_do_you_enjoy_the_most = record.partner_id.what_do_you_enjoy_the_most.ids
                record.favourite_format_of_art = record.partner_id.favourite_format_of_art.ids
                record.type_of_musician = record.partner_id.type_of_musician
                record.favourite_music = record.partner_id.favourite_music.ids
                record.which_music_will_elevate_your_mode = record.partner_id.which_music_will_elevate_your_mode
                record.favourite_genre_of_movies = record.partner_id.favourite_genre_of_movies.ids
                record.what_sports_club_are_you_member_in = record.partner_id.what_sports_club_are_you_member_in
                record.favourite_cuisines = record.partner_id.favourite_cuisines.ids
                record.favourite_sport_to_engage = record.partner_id.favourite_sport_to_engage.ids
                record.favourite_sport_to_watch = record.partner_id.favourite_sport_to_watch.ids
                record.board_games = record.partner_id.board_games.ids
                record.football_club = record.partner_id.football_club.ids
                record.team_type = record.partner_id.team_type
                record.favourite_local_destination = record.partner_id.favourite_local_destination.ids
                record.other_destination_info = record.partner_id.other_destination_info
                record.city_or_beach = record.partner_id.city_or_beach
                record.preferred_season = record.partner_id.preferred_season.ids
                record.sun_or_shade = record.partner_id.sun_or_shade
                record.arrangement_of_your_dream_vacation = record.partner_id.arrangement_of_your_dream_vacation
                record.like_to_dine = record.partner_id.like_to_dine.ids
                record.shopping_or_delivery = record.partner_id.shopping_or_delivery
                record.preferred_chocolate = record.partner_id.preferred_chocolate.ids
                record.love_pets = record.partner_id.love_pets
                record.pet_info = record.partner_id.pet_info
                record.grow_plants = record.partner_id.grow_plants
                record.enjoy_reading = record.partner_id.enjoy_reading
                record.which_book_category = record.partner_id.which_book_category
                record.favourite_color = record.partner_id.favourite_color
                record.make_up_do_you_use = record.partner_id.make_up_do_you_use
                record.might_annoy_you = record.partner_id.might_annoy_you
                record.bad_mode_while_eating = record.partner_id.bad_mode_while_eating
                record.looking_for_restaurant_menu = record.partner_id.looking_for_restaurant_menu
                record.annoying_in_hotel_rooms = record.partner_id.annoying_in_hotel_rooms
                record.compound_community_space = record.partner_id.compound_community_space
                record.hate_from_start_to_arrive = record.partner_id.hate_from_start_to_arrive
                record.make_your_life_easier = record.partner_id.make_your_life_easier
                record.living_room_more_convenient = record.partner_id.living_room_more_convenient
                record.kitchen_more_convenient = record.partner_id.kitchen_more_convenient
                record.surroundings = record.partner_id.surroundings
                record.going_shopping_in_mall = record.partner_id.going_shopping_in_mall
                record.invite_people_to_home_dinner = record.partner_id.invite_people_to_home_dinner
                record.visiting_friend = record.partner_id.visiting_friend
                record.annoying_in_clothing_store = record.partner_id.annoying_in_clothing_store
                record.fitting_rooms_in_shops = record.partner_id.fitting_rooms_in_shops
                record.is_other_local_destination = record.partner_id.is_other_local_destination

                degree_lines = []
                medical_issues = []
                record.degree_ids = False
                record.medical_issues_ids = False
                for line in record.partner_id.degree_ids:
                    degree_lines.append({
                        'degree_id': line.degree_id.id,
                        'institutions_id': line.institutions_id.id,
                        'date': line.date,
                        'partner_id': line.partner_id.id,
                        # 'lead_id': self.id,
                    })
                for line in record.partner_id.medical_issues_ids:
                    medical_issues.append({
                        'type': line.type,
                        'date': line.date,
                        'more_info': line.more_info,
                        'partner_id': line.partner_id.id,
                        # 'lead_id': self.id,
                    })
                record.degree_ids = [(0, 0, line) for line in degree_lines]
                record.medical_issues_ids = [(0, 0, line) for line in medical_issues]
