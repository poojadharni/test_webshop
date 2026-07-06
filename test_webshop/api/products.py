import frappe

@frappe.whitelist(allow_guest=True)
def get_products():

    items = frappe.get_all(
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
        limit=20
    )

    for item in items:
        price = frappe.db.get_value(
            "Item Price",
            {
                "item_code": item["name"],
                "price_list": "Standard Selling",
                "selling": 1
            },
            "price_list_rate"
        )

        item["price"] = price or 0

    return items