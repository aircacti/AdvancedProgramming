def flatten_list(nested_list: list) -> list:
    resut = []

    for item in nested_list:
        if isinstance(item, list):
            resut.extend(flatten_list(item))
        else:
            resut.append(item)

    return resut
