
def get_attr_val_recursive(object, sub_list):
    if len(sub_list) == 1:
        return getattr(object, sub_list[0])
    else:
        new_object = getattr(object, sub_list[0])
        return get_attr_val_recursive(new_object, sub_list[1:])
