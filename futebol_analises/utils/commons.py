def try_parse(value_):
    try:
        int(value_)
        return True
    except:
        return False