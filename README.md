# singleton-py

type-parameterized singleton decorator for python 3.x (PEP 695 compliant). works with all modern type-checkers. zero dependencies. 11 lines of functional code.

## INSTALL

```bash
git clone https://github.com/nk-rt/singleton-py.git
```

no dependencies. just add the repo to `PYTHONPATH` or copy `singleton/singleton.py` into your project.

## USAGE

```python
from singleton import singleton

@singleton
class Database:
    def __init__(self, host="localhost", port=5432):
        self.host = host
        self.port = port
```

just import and drop a `@singleton` decorator above your class definition. yeah, that's all there is to it.

### USAGE // TECHNICALS

```python
# all calls return the same instance. args are ignored after first init.
db1 = Database()
db2 = Database()
assert db1 is db2

# classmethods and attributes are transparently proxied.
@singleton
class Service:
    @classmethod
    def version(cls):
        return "v2.0"

Service.version()  # "v2.0"

# the original class is accessible via __wrapped__.
Database.__wrapped__  # <class 'Database'>
```

### USAGE // SEMANTICS

- **first call wins.** the instance is cached on first `__call__`. subsequent calls ignore new arguments and return the cached instance.
- **all attributes passthrough.** `__getattr__` delegates attribute lookups to the wrapped class, so `@classmethod` and static attributes work transparently.
- **underlying structure is preserved.** the undecorated class is preserved via the `__wrapped__` attribute enabling seamless backwards compatability with existing structure-dependent code and/or introspection. 

## REFERENCE

```python
singleton(cls: type[T]) -> _SingletonWrapper[T]
```

| Member | Description |
|---|---|
| `__call__(*args, **kwargs)` | returns the cached instance, creating it on first call |
| `__getattr__(name)` | proxies attribute access to the wrapped class |
| `__wrapped__` | reference to the original, undecorated class |


:)
