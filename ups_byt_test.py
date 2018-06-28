import time

ups_member_card = {
	"Andrej" : "1",
	"Roman" : "2",
	"Sasha" : "3",
	"Lina" : "4",
	"Tung" : "5",
	"Chuot" : "6",
	"Marie" : "7",
	"Linh" : "8",
	}
ups_pohlavi = {
	"1" : "",
	"2" : "",
	"3" : "a",
	"4" : "a",
	"5" : "",
	"6" : "a",
	"7" : "a",
	"8" : "",
	}
ups = {}
for c in range(len(ups_member_card)):
	for k, v in ups_member_card.items():
			ups[v] = {
				"name" : k,
				"status" : "",
				"time" : time.localtime(),
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
				"time" : time.localtime(),
				}