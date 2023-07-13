def clamp(val, min_val, max_val) :
    return min(max_val, max(min_val, val))

def floor_to_int(val) :
    # int 変換は基本 floor (切り捨て) python には型がないので
    # これで十分
    return int(val)