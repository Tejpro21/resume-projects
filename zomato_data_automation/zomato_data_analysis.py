import numpy as np
import pandas as pd

data = pd.read_csv("/Users/tejas/Desktop/Folder_of_Folders/Python_files/Datascience/Zomato.csv")
hotel_type = data['listed_in(type)'].tolist()
delivery_type = data['online_order'].tolist()
cost = data['approx_cost(for two people)'].tolist()
online = []
for i in delivery_type:
    if i == "Yes":
        online.append(i)
offline = len(delivery_type)-len(online)
online = len(online)
if online>offline:
    ordertype = "Online"
else:
    ordertype = "Offline"
hotel = []
hotel = list(set(hotel))
for i in hotel_type:
    if hotel_type.count(i) > 1:
        hotel.append(f"{hotel_type.count(i)},{i}")
hotel_type = []
for i in hotel:
    if hotel.count(i) > 1:
        if i not in hotel_type:
            hotel_type.append(i)
a = []
b = []
for i in hotel_type:
    f = i.split(",")[0]
    g = i.split(",")[-1]
    a.append(int(f))
    b.append(g)
most_popular_type = (b[a.index(max(a))])
# print(most_popular_type)
max_count = []
prices = []
for i in cost:
    if i not in prices:
        prices.append(i)
        max_count.append(cost.count(i))
most_popular_price_for_couples = prices[max_count.index(max(max_count))]

result = ["=======================================================================================",
"RESULTS:",
f"1. A greater no of restaraunts provide {ordertype} services.",
f"2. {most_popular_type} restaraunts are most favoured by the general public.",
f"3. {most_popular_price_for_couples} is the price most popular amoung couples in India.",
"======================================================================================="]
for i in result:
    print(i)