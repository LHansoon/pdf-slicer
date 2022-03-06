def router_wrapper(func):
    def wrap(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            return "something wrong with ethe stuff you typed in (`ヮ´ )σ`∀´) ﾟ∀ﾟ)σ"
    return wrap

