import random

def makelist(random_int):
    num_list = []
    for count in range(random_int):
        num_list.append(random.randint(0, 16))
    return num_list

def printlist(num_list):
	print("[", end='')
	for i in sorted(num_list):
		print (str(i), end=',')
	print("]")

def gen_list():
	for rows in range(1000):
		listlen = 1
		if random.randint(1,100) < 30:
				listlen =2
				if random.randint(1,100) < 30:
						listlen = 3
		newlist = makelist(listlen)
		printlist(newlist)
	
	

print("---------")
gen_list()
print("---------")


# def main():
#     random_int = random.randint(0, 2)
#     # print (random_int)
#     elements = makelist(random_int)
#     for i in sorted(elements):
#         print (str(i) + ",")
#

