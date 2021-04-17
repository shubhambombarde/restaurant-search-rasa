from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import smtplib
import pandas as pd




res=''

class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_search_restaurants'


    def fetch(self,loc,cuisine,price):

        #adjust the price range
        price_min = 0
        price_max = 99999
        if price == 'low':
            price_max = 300
        elif price == 'mid':
            price_min = 300
            price_max = 700
        elif price == 'high':
            price_min = 700
        else:
            price_min = 300
            price_max = 9999



        ZomatoData = pd.read_csv('zomato.csv')
        ZomatoData = ZomatoData.drop_duplicates().reset_index(drop=True)
        global cities
        cities= ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Allahabad', 'Bhubaneshwar', 'Mangalore', 'Mumbai', 'Ranchi',
                  'Patna', 'Mysore', 'Aurangabad', 'Amritsar', 'Puducherry', 'Varanasi', 'Nagpur', 'Vadodara', 'Dehradun',
                  'Vizag', 'Agra', 'Ludhiana', 'Kanpur', 'Lucknow', 'Surat', 'Kochi', 'Indore', 'Ahmedabad', 'Coimbatore',
                  'Chennai', 'Guwahati', 'Jaipur', 'Hyderabad', 'Bangalore', 'Nashik', 'Pune', 'Kolkata', 'Bhopal', 'Goa',
                  'Chandigarh', 'Ghaziabad', 'Ooty', 'Gangtok', 'Shimla']
        #

        TEMP = ZomatoData[(ZomatoData['Cuisines'].apply(lambda x: cuisine.lower() in x.lower())) & (ZomatoData['City'].apply(lambda x: loc.lower() in x.lower()))]
        return TEMP[['Restaurant Name', 'Address',  'Aggregate rating']].sort_values('Aggregate rating', ascending=False).head(5)

    def run(self, dispatcher, tracker, domain):
        cities = ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Allahabad', 'Bhubaneshwar', 'Mangalore', 'Mumbai',
                  'Ranchi',
                  'Patna', 'Mysore', 'Aurangabad', 'Amritsar', 'Puducherry', 'Varanasi', 'Nagpur', 'Vadodara',
                  'Dehradun',
                  'Vizag', 'Agra', 'Ludhiana', 'Kanpur', 'Lucknow', 'Surat', 'Kochi', 'Indore', 'Ahmedabad',
                  'Coimbatore',
                  'Chennai', 'Guwahati', 'Jaipur', 'Hyderabad', 'Bangalore', 'Nashik', 'Pune', 'Kolkata', 'Bhopal',
                  'Goa',
                  'Chandigarh', 'Ghaziabad', 'Ooty', 'Gangtok', 'Shimla']
        loc = tracker.get_slot('location')
        if loc == None:
            return dispatcher.utter_message('Location got is None')
        if loc not in cities:
            dispatcher.utter_message("We don't operate in your location")
            return [AllSlotsReset()]

        cuisine = tracker.get_slot('cuisine')
        price = tracker.get_slot('price')
        response=''
        if cuisine == None or price == None:
                dispatcher.utter_message("I didn't get all details, deafault results will be shown")
                cuisine = 'north'
                price = 'mid'

        else:
            res = self.fetch(loc,cuisine,price)
            for restaurant in res.iterrows():
                restaurant = restaurant[1]
                response = response + F"Found {restaurant['Restaurant Name']} in {restaurant['Address']} rated {restaurant['Address']} with avg cost {restaurant['Average Cost for two']} \n\n"
            SlotSet('response', response)
            dispatcher.utter_message('RESPONSE--->'+response+"\n\n\n")





class ActionSendEmail(Action):
    def name(self):
        return 'action_send_email'


    def fetch(self,loc='delhi',cuisine='north indian',price='high'):
        print(loc, cuisine, price)

        # adjust the price range
        price_min = 0
        price_max = 99999
        if price == 'low':
            price_max = 300
        elif price == 'mid':
            price_min = 300
            price_max = 700
        elif price == 'high':
            price_min = 700
        else:
            price_min = 300
            price_max = 9999


        ZomatoData = pd.read_csv('zomato.csv')
        ZomatoData = ZomatoData.drop_duplicates().reset_index(drop=True)
        global cities
        cities = ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Allahabad', 'Bhubaneshwar', 'Mangalore', 'Mumbai',
                  'Ranchi',
                  'Patna', 'Mysore', 'Aurangabad', 'Amritsar', 'Puducherry', 'Varanasi', 'Nagpur', 'Vadodara',
                  'Dehradun',
                  'Vizag', 'Agra', 'Ludhiana', 'Kanpur', 'Lucknow', 'Surat', 'Kochi', 'Indore', 'Ahmedabad',
                  'Coimbatore',
                  'Chennai', 'Guwahati', 'Jaipur', 'Hyderabad', 'Bangalore', 'Nashik', 'Pune', 'Kolkata', 'Bhopal',
                  'Goa',
                  'Chandigarh', 'Ghaziabad', 'Ooty', 'Gangtok', 'Shimla']
        #

        TEMP = ZomatoData[(ZomatoData['Cuisines'].apply(lambda x: cuisine.lower() in x.lower())) & (
            ZomatoData['City'].apply(lambda x: loc.lower() in x.lower()))]
        return TEMP[['Restaurant Name', 'Address',  'Aggregate rating']].sort_values('Aggregate rating',ascending=False).head(5)

    def run(self, dispatcher, tracker, domain):
        cities = ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Allahabad', 'Bhubaneshwar', 'Mangalore', 'Mumbai',
                  'Ranchi',
                  'Patna', 'Mysore', 'Aurangabad', 'Amritsar', 'Puducherry', 'Varanasi', 'Nagpur', 'Vadodara',
                  'Dehradun',
                  'Vizag', 'Agra', 'Ludhiana', 'Kanpur', 'Lucknow', 'Surat', 'Kochi', 'Indore', 'Ahmedabad',
                  'Coimbatore',
                  'Chennai', 'Guwahati', 'Jaipur', 'Hyderabad', 'Bangalore', 'Nashik', 'Pune', 'Kolkata', 'Bhopal',
                  'Goa',
                  'Chandigarh', 'Ghaziabad', 'Ooty', 'Gangtok', 'Shimla']

        loc = tracker.get_slot('location')
        if loc == None:
            return dispatcher.utter_message('Location got is None')
        if loc not in cities:
            dispatcher.utter_message("We don't operate in your location")
            return [AllSlotsReset()]

        cuisine = tracker.get_slot('cuisine')
        price = tracker.get_slot('price')
        response = ''
        if cuisine == None or price == None:
            dispatcher.utter_message("I didn't get all details, deafault results will be shown")
            cuisine = 'north'
            price = 'mid'

        else:
            res = self.fetch(loc, cuisine, price)
            for restaurant in res.iterrows():
                restaurant = restaurant[1]
                response = response + F"Found {restaurant['Restaurant Name']} in {restaurant['Address']} rated {restaurant['Address']} with avg cost {restaurant['Average Cost for two']} \n\n"
            SlotSet('response', response)

    def sendmail(self, MailID, res,dispatcher):

        session = smtplib.SMTP('smtp.sendgrid.net', 587)
        session.starttls()

        # Credentials are masked for Privacy
        try:
            sender_username = 'apikey'
            sender_address = 'blogbyai@admin.com'
            sender_pwd = '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'
            receiver_address = MailID
            session.login(sender_username, sender_pwd)
            text = str(res)
            message = 'From: shubhambombarde4@gmail.com\nSubject: Restaurant Search Results\n\n' + str(text)
            session.sendmail(sender_address, receiver_address, message)
            session.close()
            dispatcher.utter_message("Mail sent successfully.If you havent received your email ,please check the spam folders as well.")
        except Exception as e:
            dispatcher.utter_message("Unable to send email")
            print(e)


    def run(self, dispatcher, tracker, domain):

        loc = tracker.get_slot('location')
        cuisine = tracker.get_slot('cuisine')
        price = tracker.get_slot('price')
        cities = ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Allahabad', 'Bhubaneshwar', 'Mangalore', 'Mumbai',
                  'Ranchi',
                  'Patna', 'Mysore', 'Aurangabad', 'Amritsar', 'Puducherry', 'Varanasi', 'Nagpur', 'Vadodara',
                  'Dehradun',
                  'Vizag', 'Agra', 'Ludhiana', 'Kanpur', 'Lucknow', 'Surat', 'Kochi', 'Indore', 'Ahmedabad',
                  'Coimbatore',
                  'Chennai', 'Guwahati', 'Jaipur', 'Hyderabad', 'Bangalore', 'Nashik', 'Pune', 'Kolkata', 'Bhopal',
                  'Goa',
                  'Chandigarh', 'Ghaziabad', 'Ooty', 'Gangtok', 'Shimla']
        loc = tracker.get_slot('location')
        if loc == None:
            return dispatcher.utter_message('Location got is None')
        if loc not in cities:
            dispatcher.utter_message("We don't operate in your location")
            return [AllSlotsReset()]

        cuisine = tracker.get_slot('cuisine')
        price = tracker.get_slot('price')
        response = ''
        if cuisine == None or price == None:
            dispatcher.utter_message("I didn't get all details, deafault results will be shown")
            cuisine = 'north'
            price = 'mid'

        else:
            res = self.fetch(loc, cuisine, price)
            for restaurant in res.iterrows():
                restaurant = restaurant[1]
                response = response + F"Found {restaurant['Restaurant Name']} in {restaurant['Address']} rated {restaurant['Address']} with avg cost {restaurant['Average Cost for two']} \n\n"
        dispatcher.utter_message(response)
        MailID = tracker.get_slot('email')
        self.sendmail(MailID, response ,dispatcher)
        return [SlotSet('email', MailID)]
