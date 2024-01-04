class TryExceptDecorFactory:
    """
        A factory class with methods that
        help create tryexcept wrapper decorators
    """
    @staticmethod
    def for_methods(fallback_fn):
        """
            Used for the creation of the decorator
            for class methods

            Parameters:
            - fallback_fn (Function): Accepts "self" of
            as the first argument and an exception object
            as the second. It's call value is returned on
            raised exception

            Returns:
            Either the value of the called function that
            the decorator is used for or the fallback_fn's
            return statement
        """
        def decorator(target_fn):
            def wrapper(self, *args, **kwargs):
                try:
                    return target_fn(self, *args, **kwargs)
                except Exception as e:
                    print(e)
                    return fallback_fn(self, e)
            return wrapper

        return decorator
