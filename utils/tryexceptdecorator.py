def try_except_builder(fallback_fn):
    """
        Returns a decorator which wraps a function
        with try statement and on exception the
        decorator returns the fallback_fn's return statement

        Parameters:
        - fallback_fn (Function): The function which value
        is going to be returned on exception. It must take in
        as parameter the occured exception object

        Returns:
        - A decorator that takes in as parameter the function
        that needs to be decorated and yields the target
        function on success
    """

    def decorator(target_fn):
        def wrapper(*args, **kwargs):
            try:
                return target_fn(*args, **kwargs)
            except Exception as e:
                print(e)
                return fallback_fn(e)
        return wrapper

    return decorator
