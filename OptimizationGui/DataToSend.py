import threading

l = threading.Lock()  # mutex

my_list = []


# get the data
def get_list():
    global my_list
    return my_list[0:len(my_list)]


# insert data
def insert_data(data):
    global my_list
    my_list.append(data)


# clear the data
def clear():
    global my_list
    my_list.clear()
