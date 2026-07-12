def generate_str_method(fields):
    id_field = None
    name_field = None
    address_field = None
    first_field = None

    for fname in fields:
        if first_field is None:
            first_field = fname
        if fname.endswith("_id"):
            id_field = fname
        if fname == "name":
            name_field = fname
        if fname == "address":
            address_field = fname

    if id_field:
        if name_field:
            return f'return f"{{self.{id_field}}}: {{self.{name_field}}}"'
        elif address_field:
            return f'return f"{{self.{id_field}}}: {{self.{address_field}}}"'
        else:
            return f'return f"{{self.{id_field}}}"'
    elif name_field:
        return f'return f"{{self.{name_field}}}"'
    elif address_field:
        return f'return f"{{self.{address_field}}}"'
    else:
        return f'return f"{{self.{first_field}}}"'

