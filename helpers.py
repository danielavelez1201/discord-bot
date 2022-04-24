def db_result_to_string(l):
    result = ""
    for row in l:
        for item in row:
            result += str(item)
    return result