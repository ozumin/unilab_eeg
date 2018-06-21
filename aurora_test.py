from nanoleaf import setup
from nanoleaf import Aurora

#ipAddressList = setup.find_auroras()
#token = setup.generate_auth_token("10.0.1.2")

my_aurora = Aurora("10.0.1.2", "DR2afOWyuDMuJXoVJeM6JBq9G81ibsmo")
my_aurora.on = True
for panel in my_aurora.panel_positions:
  print(panel['panelId'])
#y_aurora = Aurora("10.0.1.2", "951DDN9PWF6kBxU4JWOyP9jxV8Q2MIHT")
#y_aurora.on = True

# panel index
# 218, 113, 23, 101, 77, 87, 86, 209, 53

effect_data = {
    "command" : "add",
    "animName": "Flash",
    "animType": "static",
    "animData": '1 113 1 0 0 255 0 10',
    "loop": True
}

my_aurora.effect_set_raw(effect_data)
