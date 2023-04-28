import os
import telebot
import time
api = os.environ['API_KEY']

bot=telebot.TeleBot(api)

invd={1:[1100,500],2:[150,1000],3:[20,300],4:[45,100],5:[20,200],6:[35,200],7:[120,100],8:[65,100],9:[150,100],10:[400,200]}
c={}
@bot.message_handler(commands=['start'])
def start(message):
  reply="Hello user welcome to the market bot. I can take your orders, show inventory, and book a delivery schedule for you"
  com="use these commands as per your convenience.\n 1./inv for checking inventory \n 2./cart for displaying your cart \n 3./status for displaying the current status of the order \n 4./confirm for confirming your order"
  bot.send_message(message.chat.id,reply)
  bot.send_message(message.chat.id,com)


@bot.message_handler(commands=['inv'])
def inv(message):
  global invd
  reply="Welcome to the inventory of the store. Feel free to buy anything, we provide high quality items with low prices assured compared to any other markets out there. Choose the item number and the quantity for adding it into the cart. EG: 3 4 => item 3 of quantity 4"
  com=" item_number --- item_name --- price --- remaining_quantity \n 1.Rice bag(25kg)   1100Rs per-bag  {}bags\n 2.oil(1kg) 150Rs  {}packets \n 3.salt(1kg) 20Rs {}packets\n 4.Milk(1L) 45Rs {}packets\n 5.Potato(1kg) 20Rs {}kgs\n 6.Tomato(1kg) 35Rs {}kgs\n 7.LUX-soap(pack of 3) 120Rs {}packs\n 8.Sprite(2.25L) 65Rs {}bottles\n 9.Icecream(1L) 150Rs {}Tubs\n 10.Atta(10kg) 400Rs {}bags\n".format(invd[1][1],invd[2][1],invd[3][1],invd[4][1],invd[5][1],invd[6][1],invd[7][1],invd[8][1],invd[9][1],invd[10][1])
  bot.send_message(message.chat.id,reply)
  bot.send_message(message.chat.id,com)

def add_to_cart(message):
  request = message.text.split()
  if len(request) < 2:
    return False
  else:
    return True


@bot.message_handler(func=add_to_cart)
def change(message):
  request = message.text.split()
  global invd
  global c
  if int(request[0]) < 1 or int(request[0]) > 10:
    bot.send_message(message.chat.id,"Select from the menu given")
  elif int(request[1]) > invd[int(request[0])][1]:
    bot.send_message(message.chat.id,"we dont have enough stock")
  else:
    try:
      c[int(request[0])][1] = c[int(request[0])][1] + int(request[1])
      c[int(request[0])][0] = invd[int(request[0])][0]*c[int(request[0])][1]
      invd[int(request[0])][1] = invd[int(request[0])][1] - int(request[1])
      bot.send_message(message.chat.id,"successfully added to cart")
    except:
      c[int(request[0])] = []
      c[int(request[0])].append(invd[int(request[0])][0]*int(request[1]))
      c[int(request[0])].append(int(request[1]))
      invd[int(request[0])][1] = invd[int(request[0])][1] - int(request[1])
      bot.send_message(message.chat.id,"successfully added to cart")


@bot.message_handler(commands=['cart'])
def cart(message):
  global c
  global invd
  cartotal = 0
  bot.send_message(message.chat.id,"item_number    amount     quantity")
  if c == {}:
     bot.send_message(message.chat.id,"cart is empty")
  for i in list(c.keys()):
    ca = str(i) + "        " + str(c[i][0]) + "        " + str(c[i][1])
    cartotal = cartotal + int(c[i][0])
    bot.send_message(message.chat.id,ca)
  total="YOUR CART TOTAL IS: " + str(cartotal)
  bot.send_message(message.chat.id,total)

@bot.message_handler(commands=['confirm'])
def confirm(message):
  bot.send_message(message.chat.id,"Your order will be confirmed in a minute, check status of your order by using /status")

@bot.message_handler(commands=['status'])
def status(message):
  status = "PENDING"
  bot.send_message(message.chat.id,status)
  time.sleep(60)
  status = "CONFIRMED"
  bot.send_message(message.chat.id,status)

@bot.message_handler(commands=['adminresetinv'])
def reset(message):
  global invd
  invd={1:[1100,500],2:[150,1000],3:[20,300],4:[45,100],5:[20,200],6:[35,200],7:[120,100],8:[65,100],9:[150,100],10:[400,200]}
bot.polling()