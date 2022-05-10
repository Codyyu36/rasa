
import email
from matplotlib.pyplot import title
import requests
import mysql.connector
import json
headers = {
    'Authorization': 'Bearer zw1OcEcPG3dMWMlplhjQYfcHmo8QHpOaz6gEgoh4J2Ty9d4dSJV0_X5XGE8Bpv3BJUpPUsz9EfolmSDuzjQvSEgy4jKR-6_5FMxwnXI35MSU2zrOCvIUmUIr9AZrYnYx',
    'Content-Type': 'application/graphql',
}
res_name_map = {}
def find_topx():
    pass


def restaurant_detail(name):
        headers = {
            'Authorization': 'Bearer zw1OcEcPG3dMWMlplhjQYfcHmo8QHpOaz6gEgoh4J2Ty9d4dSJV0_X5XGE8Bpv3BJUpPUsz9EfolmSDuzjQvSEgy4jKR-6_5FMxwnXI35MSU2zrOCvIUmUIr9AZrYnYx',
            'Content-Type': 'application/graphql',
        }
        restaurant = 'Virrueta’s Tacos'  
        location = 'San Jose'
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

            business = business + str(i['name']) + '\n' + categories + '\n' + 'phone: ' + str(i['phone']) + '\n' + 'rating: ' + str(i['rating']) + '\n' + 'price: ' + str(i['price']) + 'address: ' + str(i['location']['formatted_address'].replace('\n', ' ')) + '\n' + 'photos: ' + photos + reviews + '\n'
        print(business)





def list_detail():
    f = open('json.txt', 'r').read()
    response_dict = json.loads(f)
    res_name_map = {}
    for i in response_dict['data']['search']['business']:
        categories = ''
        for j in i['categories']:
            categories = j['title'] + '  ' + categories
            # categories = categories + '   ' + (j[title])
        business = i['name'] + '\n' + categories + '\n' + 'phone: ' + i['phone'] + '\n' + 'rating: ' + str(i['rating']) + '\n' + 'address: ' + i['location']['formatted_address'].replace('\n', ' ') + '\n\n'
        res_name_map[i['name']] = i['alias']
        print(business)
        print('')
        print('')


import textwrap

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
    #result = result.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(',', '')
    cursor.close()
    database.close()
    return result[0][0]


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

def add_user(id):
    database = mysql.connector.connect(
    host = 'localhost',
    user = 'admin',
    password = 'qwerty123',
    database = 'rasa'
    )
    name = 'Qsss'
    email = 'test@test.com'
    cursor = database.cursor()
    sql = "insert into user values (%s, '%s', '%s')" % (str(id), name, email)
    cursor.execute(sql)
    database.commit()
    result = cursor.fetchall()
    cursor.close()
    database.close()
    return []

if __name__ == '__main__':
    add_user(9)
    # list_detail()
