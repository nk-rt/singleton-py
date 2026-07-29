# singleton-py

PEP 695 type-parameterized singleton decorator. zero dependencies. 11 lines of functional code.

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

## FUNDAMENTALS

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

### SEMANTICS

- **first call wins.** the instance is cached on first `__call__`. subsequent calls ignore new arguments and return the cached instance.
- **classmethod passthrough.** `__getattr__` delegates attribute lookups to the wrapped class, so `@classmethod` and static attributes work transparently.
- **`__wrapped__`.** the undecorated class is stored on the wrapper for introspection.

## TESTS

```bash
python run_tests.py
```

| Test | What it verifies |
|---|---|
| `test_instance_identity` | `srv1 is srv2` after repeated instantiation |
| `test_class_method` | `@classmethod` resolves through the wrapper to the correct class name |
| `test_argument_immutability` | re-instantiation with new args does **not** mutate the cached instance |
| `test_attribute_identity` | a class attribute holding `Service()` points to the global singleton |
| `test_wrapped_attribute` | `__wrapped__` exists and equals the undecorated class |

all tests are plain `assert`-based. no framework required. a passing run prints `BEGIN`/`END` markers for each test; a failure raises `AssertionError` with a traceback.

## REFERENCE

```python
singleton(cls: type[T]) -> _SingletonWrapper[T]
```

| Member | Description |
|---|---|
| `__call__(*args, **kwargs)` | returns the cached instance, creating it on first call |
| `__getattr__(name)` | proxies attribute access to the wrapped class |
| `__wrapped__` | reference to the original, undecorated class |

## LICENSE

MIT