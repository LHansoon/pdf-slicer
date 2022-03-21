
def exception_holder(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return {"request-status": "fail", "Message": "Unknown error ¯\_(ツ)_/¯"}, 200
    return wrap

