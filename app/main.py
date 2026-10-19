import json
import datetime
from app.car import Car
from app.shop import Shop
from app.customer import Customer


def shop_trip():
    with open("app/config.json", "r") as f:
        data = json.load(f)

    fuel_price = data["FUEL_PRICE"]
    customers = [Customer(c["name"], c["product_cart"], c["location"], c["money"], c["car"]["fuel_consumption"]) for c in data["customers"]]
    shops = [Shop(s["name"], s["location"], s["products"]) for s in data["shops"]]

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")
        best_shop = None
        best_cost = float('inf')
        home_location = customer.location

        
        for shop in shops:
            cost = customer.calculate_trip_cost(shop, fuel_price)
            print(f"{customer.name}`s trip to the {shop.name} costs {cost}")
            if cost < best_cost:
                best_cost = cost
                best_shop = shop

        if customer.money > best_cost:
            total_shop_cost = []
            print(f"{customer.name} rides to {best_shop.name}")
            customer.location = best_shop.location
            print(f"Date: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}")
            print(f"Thanks, {customer.name}, for your purchase!")
            print("You have bought:")
            for prod, qty in customer.product_cart.items():
                price = qty * best_shop.products[prod]
                print(f"{prod}s for {round(price, 2)} dollars")
                total_shop_cost.append(price)
            print(f"Total cost is {sum(total_shop_cost)} dollars")
            print("See you again!")
            customer.location = home_location
            print(f"{customer.name} rides home")
            print(f"{customer.name} now has {customer.money - cost} dollars")
        else:
            print(f"{customer.name} doesn't have enough money to make a purchase in any shop")
