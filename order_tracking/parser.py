from bs4 import BeautifulSoup

def parse_order_info(html):
    soup = BeautifulSoup(html, "html.parser")
    order_info = {}

    # 1. Order Number
    order_number = None
    for td in soup.find_all("td"):
        if "Order number:" in td.get_text():
            span = td.find("span")
            if span:
                order_number = span.get_text(strip=True)
                break
    order_info["order_number"] = order_number

    # 2. Product (from alt attribute of product image)
    product = None
    for img in soup.find_all("img", alt=True):
        if "Product Image For:" in img["alt"]:
            product = img["alt"].replace("Product Image For: ", "").strip()
            break
    order_info["product"] = product

    # 3. SKU
    sku = None
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 2 and tds[0].get_text(strip=True) == "SKU:":
            sku = tds[1].get_text(strip=True)
            break
    order_info["sku"] = sku

    # 4. Total Price (Subtotal)
    total_price = None
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 2 and tds[0].get_text(strip=True) == "Subtotal":
            total_price = tds[1].get_text(strip=True)
            break
    order_info["total_price"] = total_price

    # 5. Quantity
    quantity = None
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 2 and tds[0].get_text(strip=True) == "Qty:":
            quantity = tds[1].get_text(strip=True)
            break
    order_info["quantity"] = quantity

    # 6. Shipped To (Shipping Address)
    shipped_to = None
    shipping_label_td = soup.find("td", string=lambda s: s and "Your order is shipping to:" in s)
    if shipping_label_td:
        # Look for the next <span> with the address, searching forward in the document
        next_span = shipping_label_td.find_next("span")
        if next_span:
            shipped_to = next_span.get_text(strip=True)
        else:
            # Fallback: look for the next <td> with text and no span
            next_td = shipping_label_td.find_next("td")
            if next_td:
                shipped_to = next_td.get_text(strip=True)
    order_info["shipped_to"] = shipped_to

    return order_info