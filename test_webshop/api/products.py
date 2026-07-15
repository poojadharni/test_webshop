import frappe


def get_product_route(item_code):
    """Get Website Item route"""

    route = frappe.db.get_value(
        "Website Item",
        {"item_code": item_code},
        "route"
    )

    return route or ""


def get_product_price(item_code):
    """Get Selling Price"""

    price = frappe.db.get_value(
        "Item Price",
        {
            "item_code": item_code,
            "price_list": "Standard Selling",
            "selling": 1
        },
        "price_list_rate"
    )

    return price or 0


@frappe.whitelist(allow_guest=True)
def get_products():

    products = frappe.get_all(
        "Item",
        filters={
            "disabled": 0,
            "has_variants": 0
        },
        fields=[
            "name",
            "item_name",
            "image",
            "description"
        ],
        order_by="creation desc",
        limit_page_length=20
    )

    for item in products:

        item["price"] = get_product_price(item["name"])
        item["route"] = get_product_route(item["name"])

    return products


@frappe.whitelist(allow_guest=True)
def get_bestsellers():

    products = frappe.get_all(
        "Item",
        filters={
            "disabled": 0,
            "has_variants": 0,
            "bestsellers": 1
        },
        fields=[
            "name",
            "item_name",
            "image",
            "description"
        ],
        order_by="creation desc"
    )

    for item in products:

        item["price"] = get_product_price(item["name"])
        item["route"] = get_product_route(item["name"])

    return products