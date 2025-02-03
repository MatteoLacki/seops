import inspect
import typing


class LazyPartial:
    def __init__(self, **providers):
        """
        Store providers for lazy evaluation.
        Each provider should be a callable returning the value.
        """
        self._providers = providers

    def register(self, name, provider):
        """Add or override an argument provider."""
        self._providers[name] = provider

    def __call__(self, func: typing.Callable, **param_to_provider: str):
        """
        Allow using this class as a decorator.
        When the decorated function is called, inject only the needed arguments.
        """

        def wrapper(*args, **kwargs):
            # Inspect function signature
            sig = inspect.signature(func)

            all_args = []
            all_kwargs = {}

            arg_idx = 0
            for param in sig.parameters:
                if param in kwargs:
                    all_kwargs[param] = kwargs[param]
                    continue

                provider_name = param_to_provider.get(param, param)
                if provider_name not in self._providers:
                    try:
                        all_args.append(args[arg_idx])
                    except IndexError as ierr:
                        raise IndexError(
                            f"{ierr}\nArgument `{param}` not provided."
                        ) from ierr
                    arg_idx += 1
                    continue

                provider = self._providers[provider_name]
                all_kwargs[param] = provider() if callable(provider) else provider

            assert len(args) == 0, "You are not using all of the provided *args."

            return func(*args, **all_kwargs)

        return wrapper


# lazy_partial = LazyPartial(x=lambda: 1, y=10)
# def test(x, y, z):
#     print(x, y, z)


# test_l = lazy_partial(test, z=13)
# test_l()
# test_l(z=14)
# test_l(z=23, w=14)
# largs._providers["x"]()
