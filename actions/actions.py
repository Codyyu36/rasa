# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from unittest import result
from matplotlib.pyplot import text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
# import json
from rasa_sdk.events import SlotSet
from datetime import datetime
import mysql.connector
from rasa_sdk.events import AllSlotsReset
import json

res_name_map = {}

class ActionReset(Action):

     def name(self) -> Text:
            return "action_reset_slots"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message("All slots have been reset")

         return [AllSlotsReset()]

def send_message(email,subject, body):
	return requests.post(
		"https://api.mailgun.net/v3/sandboxcefcaaf6412e4b46a4ed704a3c08efb4.mailgun.org/messages",
		auth=("api", "a9aafc8b16cb000e3e1563aa2143d4d4-100b5c8d-e0fded49"),
		data={"from": "RASA CHATBOT <mailgun@sandboxcefcaaf6412e4b46a4ed704a3c08efb4.mailgun.org>",
			"to": ["" + email + ""],
			"subject": "" + subject + "",
			"text": "" + body + ""})


def find_newest_user_id():

    database = mysql.connector.connect(
    host = 'localhost',
    user = 'admin',
    password = 'qwerty123',
    database = 'rasa'
    )
    cursor = database.cursor()
    sql = "select user_id from user ORDER by user_id DESC LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    database.close()
    return result[0][0] + 1

def return_use_info(id):
    database = mysql.connector.connect(
    host = 'localhost',
    user = 'admin',
    password = 'qwerty123',
    database = 'rasa'
    )
    cursor = database.cursor()
    sql = 'select * from user where user_id = ' + str(id) + ''
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    database.close()
    return result[0]

class ActionHelloWorld(Action):
     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Hello World!")
        
         return []


class ActionJoke(Action):
    def name(self) -> Text:
        return "action_joke"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        request = requests.get('http://api.icndb.com/jokes/random').json()  # make an api call
        joke = request['value']['joke']  # extract a joke from returned json response
        dispatcher.utter_message(text=joke)  # send the message back to the user
        return []


class ActionWelcome_User(Action):
    def name(self) -> Text:
        return "action_welcome_user"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id = str(next(tracker.get_latest_entity_values("id"),None))

        user_name = return_use_info(id)[1]
        user_email = return_use_info(id)[2]
        msg = 'Welcome back, ' + user_name + '. Your email is ' + user_email
        dispatcher.utter_message(text=msg)
        return [SlotSet("email", user_email)]


class ActionSaveID(Action):
    def name(self) -> Text:
        return "action_save_id"
        
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id = str(find_newest_user_id())
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')

        database = mysql.connector.connect(
        host = 'localhost',
        user = 'admin',
        password = 'qwerty123',
        database = 'rasa'
        )
        cursor = database.cursor()
        sql = "insert into user values (%s, '%s', '%s')" % (id, name, email)
        print(sql)
        cursor.execute(sql)
        database.commit()
        result = cursor.fetchall()
        cursor.close()
        database.close()
        msg = 'welcome, %s. Your id is %s, you can use that for future use by telling your id to me next time.' % (name, id)
        dispatcher.utter_message(text=msg)

        return []


class ActionSetLocation(Action):
    def name(self) -> Text:
        return "action_set_location"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tracker.latest_message['text'] 
        return [SlotSet("location", None)]


class ActionRestaurantDetail(Action):
    def name(self) -> Text:
        return "action_restaurant_detail"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        headers = {
            'Authorization': 'Bearer zw1OcEcPG3dMWMlplhjQYfcHmo8QHpOaz6gEgoh4J2Ty9d4dSJV0_X5XGE8Bpv3BJUpPUsz9EfolmSDuzjQvSEgy4jKR-6_5FMxwnXI35MSU2zrOCvIUmUIr9AZrYnYx',
            'Content-Type': 'application/graphql',
        }
        restaurant = tracker.get_slot('restaurant_name')   
        location = tracker.get_slot('location')
        new_data = '''
        {
            search(term: "%s", location: "%s", limit: 1) {
                total
                business {
                name
                id
                url
                phone
                location {
                    formatted_address
                }
                hours {
                    is_open_now
                }
                display_phone
                reviews {
                    rating
                    text
                }
                categories {
                            title
                            alias
                }
                rating
                price
                photos
                }
            }
        } ''' % (restaurant, location)
        
        response = requests.post('https://api.yelp.com/v3/graphql', headers=headers, data=new_data.encode('utf-8'))
        response_dict = json.loads(response.text)
        business = ''
        for i in response_dict['data']['search']['business']:
            categories = ''
            reviews = ''
            photos = ''
            for k in i['reviews']:
                reviews = 'rating: ' + str(k['rating']) + '\n' + k['text'] + '\n\n' + reviews
            reviews = 'reviews: \n' + reviews
            for j in i['categories']:
                categories = j['title'] + '  ' + categories

            for m in i['photos']:
                photos = photos + m + '\n'

            business = business + str(i['name']) + '\n' + categories + '\n' + 'phone: ' + str(i['phone']) + '\n' + 'rating: ' + str(i['rating']) + '\n' + 'price: ' + str(i['price']) + '\naddress: ' + str(i['location']['formatted_address'].replace('\n', ' ')) + '\n' + 'photos: ' + photos + reviews + '\n'

    
        dispatcher.utter_message(text=business)

        return []


class ActionAskEmail(Action):
    def name(self) -> Text:
        return "action_ask_if_email"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        headers = {
            'Authorization': 'Bearer zw1OcEcPG3dMWMlplhjQYfcHmo8QHpOaz6gEgoh4J2Ty9d4dSJV0_X5XGE8Bpv3BJUpPUsz9EfolmSDuzjQvSEgy4jKR-6_5FMxwnXI35MSU2zrOCvIUmUIr9AZrYnYx',
            'Content-Type': 'application/graphql',
        }
        restaurant = tracker.get_slot('restaurant_name')   
        location = tracker.get_slot('location')
        new_data = '''
        {
            search(term: "%s", location: "%s", limit: 1) {
                total
                business {
                name
                id
                url
                phone
                location {
                    formatted_address
                }
                hours {
                    is_open_now
                }
                display_phone
                reviews {
                    rating
                    text
                }
                categories {
                            title
                            alias
                }
                rating
                price
                photos
                }
            }
        } ''' % (restaurant, location)
        
        response = requests.post('https://api.yelp.com/v3/graphql', headers=headers, data=new_data.encode('utf-8'))
        response_dict = json.loads(response.text)
        business = ''
        for i in response_dict['data']['search']['business']:
            categories = ''
            reviews = ''
            photos = ''
            for k in i['reviews']:
                reviews = 'rating: ' + str(k['rating']) + '\n' + k['text'] + '\n\n' + reviews
            reviews = 'reviews: \n' + reviews
            for j in i['categories']:
                categories = j['title'] + '  ' + categories

            for m in i['photos']:
                photos = photos + m + '\n'

            business = business + str(i['name']) + '\n' + categories + '\n' + 'phone: ' + str(i['phone']) + '\n' + 'rating: ' + str(i['rating']) + '\n' + 'price: ' + str(i['price']) + '\naddress: ' + str(i['location']['formatted_address'].replace('\n', ' ')) + '\n' + 'photos: ' + photos + reviews + '\n'

        email = tracker.get_slot('email')
        if email is None:
            dispatcher.utter_message(text='provide me your name and email please')
            dispatcher.utter_message(text='what is your name?')
        else:
            dispatcher.utter_message(text='email found associates to your id: ' + email)
            send_message(email, 'RASA chatbot', business)
            dispatcher.utter_message(text='location sent to your email.')

            id = tracker.get_slot('id')   
            food = tracker.get_slot('food_type')
            database = mysql.connector.connect(
            host = 'localhost',
            user = 'admin',
            password = 'qwerty123',
            database = 'rasa'
            )
            cursor = database.cursor()
            sql = "insert into history values (%s, '%s')" % (str(id), food)
            cursor.execute(sql)
            database.commit()
            result = cursor.fetchall()
            cursor.close()
            database.close()
        return []


class ActionSendEmail(Action):
    def name(self) -> Text:
        return "action_send_email"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        id = tracker.get_slot('id')   
        food = tracker.get_slot('food_type')

        database = mysql.connector.connect(
        host = 'localhost',
        user = 'admin',
        password = 'qwerty123',
        database = 'rasa'
        )
        cursor = database.cursor()
        sql = "insert into history values (%s, '%s')" % (str(id), food)
        cursor.execute(sql)
        database.commit()
        result = cursor.fetchall()
        cursor.close()
        database.close()


        headers = {
            'Authorization': 'Bearer zw1OcEcPG3dMWMlplhjQYfcHmo8QHpOaz6gEgoh4J2Ty9d4dSJV0_X5XGE8Bpv3BJUpPUsz9EfolmSDuzjQvSEgy4jKR-6_5FMxwnXI35MSU2zrOCvIUmUIr9AZrYnYx',
            'Content-Type': 'application/graphql',
        }
        restaurant = tracker.get_slot('restaurant_name')   
        location = tracker.get_slot('location')
        new_data = '''
        {
            search(term: "%s", location: "%s", limit: 1) {
                total
                business {
                name
                id
                url
                phone
                location {
                    formatted_address
                }
                hours {
                    is_open_now
                }
                display_phone
                reviews {
                    rating
                    text
                }
                categories {
                            title
                            alias
                }
                rating
                price
                photos
                }
            }
        } ''' % (restaurant, location)
        
        response = requests.post('https://api.yelp.com/v3/graphql', headers=headers, data=new_data.encode('utf-8'))
        response_dict = json.loads(response.text)
        business = ''
        for i in response_dict['data']['search']['business']:
            categories = ''
            reviews = ''
            photos = ''
            for k in i['reviews']:
                reviews = 'rating: ' + str(k['rating']) + '\n' + k['text'] + '\n\n' + reviews
            reviews = 'reviews: \n' + reviews
            for j in i['categories']:
                categories = j['title'] + '  ' + categories

            for m in i['photos']:
                photos = photos + m + '\n'

            business = business + str(i['name']) + '\n' + categories + '\n' + 'phone: ' + str(i['phone']) + '\n' + 'rating: ' + str(i['rating']) + '\n' + 'price: ' + str(i['price']) + '\naddress: ' + str(i['location']['formatted_address'].replace('\n', ' ')) + '\n' + 'photos: ' + photos + reviews + '\n'

        email = tracker.get_slot('email')
        send_message(email, 'RASA chatbot', business)
        dispatcher.utter_message(text='location sent to your email.')
        return []


class ActionCheckRestaurants(Action):
    
    def name(self) -> Text:
        return "action_check_restaurants"

    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        headers = {
            'Authorization': 'Bearer zw1OcEcPG3dMWMlplhjQYfcHmo8QHpOaz6gEgoh4J2Ty9d4dSJV0_X5XGE8Bpv3BJUpPUsz9EfolmSDuzjQvSEgy4jKR-6_5FMxwnXI35MSU2zrOCvIUmUIr9AZrYnYx',
            'Content-Type': 'application/graphql',
        }

        location = tracker.get_slot('location')
        food = tracker.get_slot('food_type')
        
        new_data = ''' {
                        search(term: "%s", location: "%s", limit: 5) {
                        total
                        business {
                        name
                        alias
                        hours {
                            is_open_now
                        }
                        location {
                            formatted_address
                        } 
                        categories {
                            title
                            alias
                        }
                        phone
                        rating
                        }
                    }
                }
                ''' % (food, location)
 

        response = requests.post('https://api.yelp.com/v3/graphql', headers=headers, data=new_data)
        response_dict = json.loads(response.text)
        res_name_map = {}
        business = ''
        for i in response_dict['data']['search']['business']:
            categories = ''
            for j in i['categories']:
                categories = j['title'] + '  ' + categories

            business = business + i['name'] + '\n' + categories + '\n' + 'phone: ' + i['phone'] + '\n' + 'rating: ' + str(i['rating']) + '\n' + 'address: ' + i['location']['formatted_address'].replace('\n', ' ') + '\n\n\n'
        res_name_map[i['name']] = i['alias']


        dispatcher.utter_message(text=business)
        return []


class ActionTellTime(Action):
    def name(self) -> Text:
        return "action_tell_time"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        msg = "current time is " + str(current_time)
        # print("Current Time =", current_time)
        dispatcher.utter_message(text = msg)
        return []



""""
class ActionCheckRestaurants(Action):
   def name(self) -> Text:
      return "action_check_restaurants"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

      cuisine = tracker.get_slot('cuisine')
      q = "select * from restaurants where cuisine='{0}' limit 1".format(cuisine)
      result = db.query(q)

      return [SlotSet("matches", result if result is not None else [])]

if __name__ == '__main__':
    ac = ActionJoke()
    ac.run()
"""