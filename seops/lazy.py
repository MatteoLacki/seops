import inspect
import typing


class LazyPartial:
    def __init__(self, **providers):
        """
        Store providers for lazy evaluation.
        Callable providers will be called.
        If you want those callable providers to be cached, wrap them in functools.cache yourself.
        """
        self._providers = {}
        for name, prov in providers.items():
            self.register(name, prov)

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


class CommonArguments:
    """
    Keep a collection of lazily evaluated (but not necessarily cached) objects.
    Provide only callables as input.
    """

    def __init__(self, **providers):
        self._providers = {}
        for name, provider in providers.items():
            self.register(name, provider)

    def register(self, name, provider):
        """Add or override an argument provider."""
        assert callable(provider)
        self._providers[name] = provider

    def get_kwargs(self, foo, renaming={}, **foo_kwargs):
        kwargs = {}
        for param in inspect.signature(foo).parameters:
            if param in foo_kwargs:
                kwargs[param] = foo_kwargs[param]
                continue

            provider_name = renaming.get(param, param)
            if provider_name not in self._providers:
                continue

            provider = self._providers[provider_name]
            kwargs[param] = provider()

        return kwargs

    def get_args(self, foo, renaming={}, *foo_args, **foo_kwargs):
        return list(self.get_kwargs(foo, renaming, *foo_args, **foo_kwargs).values())


# lazy_partial = LazyPartial(x=lambda: 1, y=10)
# def test(x, y, z):
#     print(x, y, z)


# test_l = lazy_partial(test, z=13)
# test_l()
# test_l(z=14)
# test_l(z=23, w=14)
# largs._providers["x"]()
