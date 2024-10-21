from finder.models import LookupTable
from memoization import cached
import datetime


@cached
def get_lookup_value(master_key, key)->str:
    """
    Returns the lookup value when master key and key are given.
    """
    lookup_obj = LookupTable.objects.filter(master_key=master_key, key=key).first()
    print(datetime.datetime.now())
    if lookup_obj is not None:
        return lookup_obj.value
    return None


@cached
def get_lookup_key(master_key, value)->int:
    """
    Returns the lookup key when master key and value are given.
    """
    lookup_obj = LookupTable.objects.filter(master_key=master_key, value=value).first()
    if lookup_obj is not None:
        return lookup_obj.key
    return None