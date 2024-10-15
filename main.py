import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("ACCESS_TOKEN")
base_url = "https://steve-test1.myshopify.com/admin/api/2024-01/"
headers = {
    "X-Shopify-Access-Token": f"{access_token}",
    "Content-Type": "application/json",
}


def get_products():
    params = {}
    response = requests.get(
        f"{base_url}/products.json",
        params=params,
        headers=headers,
    )
    products = response.json().get("products", [])
    return products


def get_custom_collections():
    params = {}
    response = requests.get(
        f"{base_url}/custom_collections.json",
        params=params,
        headers=headers,
    )
    custom_collections = response.json().get("custom_collections", [])
    return custom_collections


def get_customers():
    params = {}
    response = requests.get(
        f"{base_url}/customers.json",
        params=params,
        headers=headers,
    )
    customers = response.json().get("customers", [])
    return customers


def get_orders():
    params = {}
    response = requests.get(
        f"{base_url}/orders.json",
        params=params,
        headers=headers,
    )
    orders = response.json().get("orders", [])
    return orders


def get_variants(product):
    variants = []
    for variant in product["variants"]:
        variants.append(
            {
                "id": variant["id"],
                "price": variant["price"],
                "inventory_item_id": variant["inventory_item_id"],
                "inventory_quantity": variant["inventory_quantity"],
                "old_inventory_quantity": variant["old_inventory_quantity"],
            }
        )
    return variants


def create_product_no_option():
    json_data = {
        "product": {
            "title": "Product no option",
            "status": "draft",
        },
    }
    response = requests.post(
        f"{base_url}/products.json",
        headers=headers,
        json=json_data,
    )
    if response.status_code == 201:
        print("Create product no option success")
    else:
        print("Create product no option failed")


def create_product_have_option():
    json_data = {
        "product": {
            "title": "Product have option",
            "variants": [
                {
                    "option1": "Blue",
                    "option2": "Medium",
                    "price": "150000.00",
                },
                {
                    "option1": "Black",
                    "option2": "Medium",
                    "price": "150000.00",
                },
                {
                    "option1": "Blue",
                    "option2": "Large",
                    "price": "160000.00",
                },
                {
                    "option1": "Black",
                    "option2": "Large",
                    "price": "160000.00",
                },
            ],
            "options": [
                {
                    "name": "Color",
                    "values": [
                        "Blue",
                        "Black",
                    ],
                },
                {
                    "name": "Size",
                    "values": [
                        "Medium",
                        "Large",
                    ],
                },
            ],
        },
    }
    response = requests.post(
        f"{base_url}/products.json",
        headers=headers,
        json=json_data,
    )
    if response.status_code == 201:
        print("Create product have option success")
    else:
        print("Create product have option failed")


def create_custom_collection():
    products = get_products()
    valid_product_id = products[0]["id"] if products else None
    if valid_product_id:
        json_data = {
            "custom_collection": {
                "title": "IPods",
                "collects": [
                    {
                        "product_id": valid_product_id,
                    },
                ],
            },
        }
        response = requests.post(
            f"{base_url}/custom_collections.json",
            headers=headers,
            json=json_data,
        )
        if response.status_code == 201:
            print("Create custom collection success")
        else:
            print("Create custom collection failed")
    else:
        print("No products found")


def create_customer():
    json_data = {
        "customer": {
            "first_name": "Steve",
            "last_name": "Mạnh Đỗ",
            "email": "steve@litextension.com",
            "phone": "0866956913",
            "verified_email": True,
            "addresses": [
                {
                    "address1": "Nam Tu Liem, Ha Noi",
                    "city": "Ha Noi",
                    "province": "Nam Tu liem",
                    "phone": "0123456789",
                    "zip": "190000",
                    "last_name": "Address",
                    "first_name": "Address",
                    "country": "VN",
                },
            ],
            "password": "12345678",
            "password_confirmation": "12345678",
            "send_email_welcome": False,
        },
    }

    response = requests.post(
        f"{base_url}/customers.json",
        headers=headers,
        json=json_data,
    )
    if response.status_code == 201:
        print("Create customer success")
    else:
        print("Create customer failed")


def create_order():
    products = get_products()
    customers = get_customers()
    first_product = products[0] if products else None
    valid_customer_id = customers[0]["id"] if customers else None
    quantity = 1
    json_data = {
        "order": {
            "line_items": [
                {
                    "title": "Test Api Order",
                    "variant_id": first_product["id"],
                    "quantity": quantity,
                    "price": first_product["variants"][0]["price"] * quantity,
                },
            ],
            "customer": {
                "id": valid_customer_id,
            },
            "financial_status": "pending",
        },
    }

    response = requests.post(
        f"{base_url}/orders.json",
        headers=headers,
        json=json_data,
    )
    if response.status_code == 201:
        print("Create order success")
    else:
        print("Create order failed")


def update_product():
    products = get_products()
    for product in products:
        product_id = product["id"]
        variants = get_variants(product)
        variants[0]["price"] = 100000
        json_data = {
            "product": {
                "id": product_id,
                "variants": variants,
                "images": [
                    {
                        "src": "https://media.istockphoto.com/id/1328049157/photo/mens-short-sleeve-t-shirt-mockup-in-front-and-back-views.jpg?s=612x612&w=0&k=20&c=1_zfKF73GEFp5RtLEyQQn8ZH5UB5THiom2pBSXb9-Uw="
                    },
                    {
                        "src": "https://media.istockphoto.com/id/488160041/photo/mens-shirt.jpg?s=612x612&w=0&k=20&c=xVZjKAUJecIpYc_fKRz_EB8HuRmXCOOPOtZ-ST6eFvQ=",
                    },
                ],
            },
        }
        response = requests.put(
            f"{base_url}/products/{product_id}.json",
            headers=headers,
            json=json_data,
        )
        if response.status_code == 200:
            print("Update product image, price success")
        else:
            print("Update product image, price failed")


def enable_inventory_tracking(inventory_item_id):
    json_data = {
        "inventory_item": {
            "id": inventory_item_id,
            "tracked": True,
        },
    }
    response = requests.put(
        f"{base_url}/inventory_items/{inventory_item_id}.json",
        headers=headers,
        json=json_data,
    )
    if response.status_code == 200:
        print(f"Inventory tracking enabled for item {inventory_item_id}")
    else:
        print(f"Failed to enable inventory tracking for item {inventory_item_id}")
        print(response.json())


def update_inventory_quantity(inventory_item_id, new_quantity):
    response = requests.get(
        f"{base_url}/locations.json",
        headers=headers,
    )
    locations = response.json().get("locations", [])
    if not locations:
        print("No locations found.")
        return

    location_id = locations[0]["id"]
    enable_inventory_tracking(inventory_item_id)
    json_data = {
        "location_id": location_id,
        "inventory_item_id": inventory_item_id,
        "available": new_quantity,
    }
    response = requests.post(
        f"{base_url}/inventory_levels/set.json",
        headers=headers,
        json=json_data,
    )
    if response.status_code == 200:
        print(f"Inventory updated successfully for item {inventory_item_id}")
    else:
        print(f"Failed to update inventory for item {inventory_item_id}")
        print(response.json())


def update_product_quantities(new_quantities):
    products = get_products()
    for product in products:
        variants = get_variants(product)
        for variant in variants:
            inventory_item_id = variant["inventory_item_id"]
            if inventory_item_id in new_quantities:
                new_quantity = new_quantities[inventory_item_id]
                update_inventory_quantity(inventory_item_id, new_quantity)


def delete_order(order_id):
    response = requests.delete(
        f"{base_url}/orders/{order_id}.json",
        headers=headers,
    )
    if response.status_code == 200:
        print(f"Delete order success")
    else:
        print(f"Delete order failed")


def delete_customer(customer_id):
    response = requests.delete(
        f"{base_url}/customers/{customer_id}.json",
        headers=headers,
    )
    if response.status_code == 200:
        print(f"Delete customer success")
    else:
        print(f"Delete customer failed")


def delete_custom_collection(collection_id):
    response = requests.delete(
        f"{base_url}/custom_collections/{collection_id}.json",
        headers=headers,
    )
    if response.status_code == 200:
        print(f"Delete custom collection success")
    else:
        print(f"Delete custom collection failed")


def delete_product(product_id):
    response = requests.delete(
        f"{base_url}/products/{product_id}.json",
        headers=headers,
    )
    if response.status_code == 200:
        print(f"Delete product success")
    else:
        print(f"Delete product failed")


create_product_have_option()
create_product_no_option()
create_custom_collection()
create_customer()
time.sleep(10)
create_order()

#update product image, price
update_product()

# update product inventory
products = get_products()
new_quantities = {products[0]["variants"][0]["inventory_item_id"]: 20}
update_product_quantities(new_quantities)

# delete all products, orders, customers, custom collection
custom_collections = get_custom_collections()
for custom_collection in custom_collections:
    delete_custom_collection(custom_collection["id"])

orders = get_orders()
for order in orders:
    delete_order(order["id"])

time.sleep(10)
customers = get_customers()
for customer in customers:
    delete_customer(customer["id"])

products = get_products()
for product in products:
    delete_product(product["id"])
