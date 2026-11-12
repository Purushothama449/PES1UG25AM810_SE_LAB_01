
def mask_imei(imei):
    """
    Removes dashes and spaces, then hides all but the last four characters.
    Returns an empty string for invalid input.
    """
    if not isinstance(imei, str):
        return ""

    imei = imei.replace("-", "").replace(" ", "")

    return "*" * max(0, len(imei) - 4) + imei[-4:]


def parse_parts_order(text):
    """
    Parses 'screen x1; battery x2' into a dictionary.
    Invalid entries are safely ignored.
    """
    order = {}

    if not isinstance(text, str):
        return order

    for item in text.split(";"):
        if "x" not in item:
            continue

        part, qty = item.split("x", 1)
        part = part.strip()
        qty = qty.strip()

        if not part or not qty:
            continue

        try:
            quantity = int(qty)
            if quantity > 0:
                order[part] = quantity
        except ValueError:
            continue

    return order


def parse_model(text):
    """
    Splits phone brand and model into a tuple.
    Returns empty values for invalid input.
    """
    if not isinstance(text, str):
        return "", ""

    parts = text.strip().split(maxsplit=1)

    if len(parts) != 2:
        return "", ""

    brand, model = parts

    if not brand or not model:
        return "", ""

    return brand.title(), model.strip()


def main():
    print("==== Running mask_imei ====")
    value = input("Enter an IMEI number (e.g. 35-209900-176148-1): ")
    print("Masked IMEI:", mask_imei(value))

    print("\n==== Running parse_parts_order ====")
    value = input(
        "Enter parts and quantities as PART xQTY separated by ; "
        "(e.g. screen x1; battery x2): "
    )
    print("Parts order:", parse_parts_order(value))

    print("\n==== Running parse_model ====")
    value = input("Enter the phone brand and model (e.g. Samsung Galaxy S23): ")
    print("Brand and model:", parse_model(value))


if __name__ == "__main__":
    main()
