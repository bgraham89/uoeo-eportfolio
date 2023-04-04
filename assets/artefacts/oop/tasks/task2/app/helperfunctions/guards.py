'''Helper functions for adding constraints to function parameters.'''

import logging
import traceback

def arg_cond(params, condition):
    '''Function to apply a constraint on params'''
    try:
        assert condition(*params)
    except TypeError as e:
        err_message = (f"{condition} has mismatch with inputs: {params}.")
        raise TypeError(err_message).with_traceback(e.__traceback__)
    except AssertionError as e:
        err_message = f"{params} didn't pass {condition}."
        raise AssertionError(err_message).with_traceback(e.__traceback__)
    except Exception as e:
        logging.error(traceback.format_exc())  #educational
        err_message = "Unknown error."
        raise Exception(err_message).with_traceback(e.__traceback__)
    return True
