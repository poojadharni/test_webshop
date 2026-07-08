import frappe

@frappe.whitelist(allow_guest=True)
def add_to_cart(item_code, qty=1):
    if frappe.session.user == "Guest":
        frappe.throw("Please login to add items to cart")

    from webshop.webshop.shopping_cart.cart import (
        _get_cart_quotation,
        get_party
    )

    party = get_party()
    quotation = _get_cart_quotation(party)

    # check if item already exists
    item_found = False

    for item in quotation.items:
        if item.item_code == item_code:
            item.qty = item.qty + int(qty)
            item_found = True
            break

    # add new item
    if not item_found:
        quotation.append("items", {
            "item_code": item_code,
            "qty": int(qty)
        })

    quotation.save(ignore_permissions=True)
    frappe.db.commit()

    cart_count = sum(item.qty for item in quotation.items)

    return {
        "message": "Item added to cart",
        "cart_count": cart_count
    }


@frappe.whitelist(allow_guest=True)
def get_cart_count():
    if frappe.session.user == "Guest":
        return 0

    from webshop.webshop.shopping_cart.cart import _get_cart_quotation, get_party

    party = get_party()
    quotation = _get_cart_quotation(party)

    if quotation and quotation.get("items"):
        return sum(item.qty for item in quotation.items)

    return 0

@frappe.whitelist(allow_guest=True)
def get_wishlist_count():
    if frappe.session.user == "Guest":
        return 0

    wishlist_items = frappe.get_all(
        "Wishlist Item",
        filters={"owner": frappe.session.user},
        pluck="name"
    )
    return len(wishlist_items)