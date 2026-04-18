def get_shard(doc):

    if "leave" in doc.lower():
        return "hr_leave"
    elif "salary" in doc.lower():
        return "hr_salary"
    else:
        return "hr_general"