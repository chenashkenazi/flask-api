from operator import index
from flask import Flask, Request
from flask_restful import Api, Resource, reqparse
import requests
import json
import datetime
import time

from requests.api import request

app = Flask(__name__)
api = Api(app)

def get_data_from_api(t):
  '''
  while t > 0:
    mins = t // 60
    secs = t % 60
    timer = '{:02d}:{02d}'.format(mins, secs)
    time.sleep(1)
    t -= 1
  '''
  req = requests.get('https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup')
  data = json.loads(req.content)
  return data['Data']


data = get_data_from_api(3600)
drinks_data = data['categoriesList'][5]['dishList']
pizzas_data = data['categoriesList'][3]['dishList']
desserts_data = data['categoriesList'][4]['dishList']

order_post_args = reqparse.RequestParser()
order_post_args.add_argument("drinks", action='append')
order_post_args.add_argument("desserts", action='append')
order_post_args.add_argument("pizzas", action='append')

class Drink(Resource):

  def get(self, drink_id=None):
    output = ''
    if not drink_id:
       for drink in drinks_data:
        output += 'ID: ' + str(drink['dishId']) + ' '
        output += 'Name: ' + str(drink['dishName']) + ' '
        output += 'Description: ' + str(drink['dishDescription']) + ' '
        output += 'Price: ' + str(drink['dishPrice']) + ' '
    else:
      for drink in drinks_data:
        if drink['dishId'] == int(drink_id):
          output += 'ID: ' + str(drink['dishId']) + ' '
          output += 'Name: ' + str(drink['dishName']) + ' '
          output += 'Description: ' + str(drink['dishDescription']) + ' '
          output += 'Price: ' + str(drink['dishPrice']) + ' '
          break
  
    return output

class Pizza(Resource):

  def get(self, pizza_id=None):
    output = ''
    if not pizza_id:
       for pizza in pizzas_data:
        output += 'ID: ' + str(pizza['dishId']) + ' '
        output += 'Name: ' + str(pizza['dishName']) + ' '
        output += 'Description: ' + str(pizza['dishDescription']) + ' '
        output += 'Price: ' + str(pizza['dishPrice']) + ' '
    else:
      for pizza in pizzas_data:
        if pizza['dishId'] == int(pizza_id):
          output += 'ID: ' + str(pizza['dishId']) + ' '
          output += 'Name: ' + str(pizza['dishName']) + ' '
          output += 'Description: ' + str(pizza['dishDescription']) + ' '
          output += 'Price: ' + str(pizza['dishPrice']) + ' '
          break
  
    return output

class Dessert(Resource):

  def get(self, dessert_id=None):
    output = ''
    if not dessert_id:
       for dessert in desserts_data:
        output += 'ID: ' + str(dessert['dishId']) + ' '
        output += 'Name: ' + str(dessert['dishName']) + ' '
        output += 'Description: ' + str(dessert['dishDescription']) + ' '
        output += 'Price: ' + str(dessert['dishPrice']) + ' '
    else:
      for dessert in desserts_data:
        if dessert['dishId'] == int(dessert_id):
          output += 'ID: ' + str(dessert['dishId']) + ' '
          output += 'Name: ' + str(dessert['dishName']) + ' '
          output += 'Description: ' + str(dessert['dishDescription']) + ' '
          output += 'Price: ' + str(dessert['dishPrice']) + ' '
          break
  
    return output

class Order(Resource):
  def post(self):
    '''
    request_data = Request.json()
    print(request_data)
    return request_data
    '''
    total_sum = 0
    args = order_post_args.parse_args()

    if args['drinks']:
      for drink_id in args['drinks']:
        for dr in drinks_data:
          if dr['dishId'] == int(drink_id):
            total_sum += dr['dishPrice']
    
    if args['pizzas']:
      for pizza_id in args['pizzas']:
        for p in pizzas_data:
          if p['dishId'] == int(pizza_id):
            total_sum += p['dishPrice']

    if args['desserts']:
      for dessert_id in args['desserts']:
        for de in desserts_data:
          if de['dishId'] == int(dessert_id):
            total_sum += de['dishPrice']
          
    return total_sum


api.add_resource(Drink, '/drinks', '/drinks/<int:drink_id>')
api.add_resource(Pizza, '/pizzas', '/pizzas/<int:pizza_id>')
api.add_resource(Dessert, '/desserts', '/desserts/<int:dessert_id>')
api.add_resource(Order, '/order')

if __name__ == "__main__":
  app.run(debug=True)