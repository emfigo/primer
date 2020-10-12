from primer import exceptions

def slice(kls, details: dict) -> dict:
    sliced_details = {}

    for k in kls.MANDATORY_FIELDS:
        if details.get(k) is not None:
            sliced_details[k] = details[k]
        else:
            raise getattr(exceptions, f"Invalid{kls.__name__.replace('Create','')}")

    for k in kls.OPTIONAL_FIELDS:
        sliced_details[k] = details.get(k)


    return sliced_details
