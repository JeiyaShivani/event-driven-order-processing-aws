def lambda_handler(event, context):
    product = event.get("product")
    quantity = event.get("quantity")
    price = event.get("price")
    customer_id = event.get("customer_id")

    if not product or not customer_id:
        raise Exception("Missing product or customer_id")

    if quantity is None or int(quantity) <= 0:
        raise Exception("Quantity must be > 0")

    if price is None or float(price) <= 0:
        raise Exception("Price must be > 0")

    #return same structure so next lambda can access product directly
    return {
        **event,
        "validated": True
    }
