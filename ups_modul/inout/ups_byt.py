import time
import requests

# def roman_fn(card_status):
#     if card_status['status'] == "OUT":
#         requests.post("http://0.0.0.0:5000/leave")
#     else:
#         requests.post("http://0.0.0.0:5000/home")

# ups_member_callback_dict = {
# "111111112255111133554444772828": [roman_fn]
# }


ups_member_card = {
	"Andrej" : "11111111225511112277101033332828",
	"Roman" : "111111112255111133554444772828",
	"Sasha" : "111111112255111110101111331111772828",
	"Lina" : "111111112255111199554455992828",
	"Tung" : "11111111225511113366881111222828",
	"Chuot" : "111111112255111133442222662828",
	"Marie" : "111111112255111188992277222828",
	"Linh" : "111111112255111199555544332828",
	"Tu" : "111111112244994477551010332828",
	"Rudolf" : "1111111122551111229911111010992828",
	"Anna" : "111111112244881010995555882828",
	}
ups_pohlavi = {
	"11111111225511112277101033332828" : "",
	"111111112255111133554444772828" : "",
	"111111112255111110101111331111772828" : "a",
	"111111112255111199554455992828" : "a",
	"11111111225511113366881111222828" : "",
	"111111112255111133442222662828" : "a",
	"111111112255111188992277222828" : "a",
	"111111112255111199555544332828" : "",
	"111111112244994477551010332828" : "a",
	"1111111122551111229911111010992828" : "",
	"111111112244881010995555882828" : "a",
	}
ups = {}
for c in range(len(ups_member_card)):
	for k, v in ups_member_card.items():
			ups[v] = {
				"name" : k,
				"status" : "OUT",
				"time" : time.localtime()
				}
ups_hoste = {}
ups_hoste_card = {
	"host1" : "1",
	"host2" : "2",
	"host3" : "3",
	"host4" : "4",
	}
for c in range(len(ups_hoste_card)):
	for k, v in ups_hoste_card.items():
			ups_hoste[v] = {
				"name" : k,
				"status" : "OUT",
				"time" : time.localtime()
				}
