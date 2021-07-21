from numpy import log as ln

def generate_ban_time_string(permission_time):
    permission_time = int(permission_time)

    year = permission_time // (365 * 24 * 3600)
    permission_time = permission_time % (365 * 24 * 3600)
    month = permission_time // (30 * 24 * 3600)
    permission_time = permission_time % (30 * 24 * 3600)
    week = permission_time // (7 * 24 * 3600)
    permission_time = permission_time % (7 * 24 * 3600)
    day = permission_time // (24 * 3600)
    permission_time = permission_time % (24 * 3600)
    hour = permission_time // 3600
    permission_time %= 3600
    minute = permission_time // 60
    permission_time %= 60
    second = permission_time


    ban_string = str()
    if year > 0:
        if year > 1:
            ban_string += f"{year} years, "
        else:
            ban_string += "1 year, "
    if month > 0:
        if month > 1:
            ban_string += f"{month} months, "
        else:
            ban_string += "1 month, "
    if week > 0:
        if week > 1:
            ban_string += f"{week} weeks, "
        else:
            ban_string += "1 week, "
    if day > 0:
        if day > 1:
            ban_string += f"{day} days, "
        else:
            ban_string += "1 day, "
    if hour > 0:
        if hour > 1:
            ban_string += f"{hour} hours, "
        else:
            ban_string += "1 hour, "
    if minute > 0:
        if minute > 1:
            ban_string += f"{minute} minutes"
        else:
            ban_string += "1 minute"
    if second > 1:
        ban_string += f", and {second} seconds"
    
    elif second == 1:
        ban_string += ", and 1 second"


    return ban_string