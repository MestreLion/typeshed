import io
import sys
from _typeshed import BytesPath, GenericPath, Self, StrPath, WriteableBuffer
from collections.abc import Iterable, Iterator
from types import TracebackType
from typing import IO, Any, AnyStr, Generic, overload
from typing_extensions import Literal, TypeAlias

if sys.version_info >= (3, 9):
    from types import GenericAlias

__all__ = [
    "NamedTemporaryFile",
    "TemporaryFile",
    "SpooledTemporaryFile",
    "TemporaryDirectory",
    "mkstemp",
    "mkdtemp",
    "mktemp",
    "TMP_MAX",
    "gettempprefix",
    "tempdir",
    "gettempdir",
    "gettempprefixb",
    "gettempdirb",
]

# global variables
TMP_MAX: int
tempdir: str | None
template: str

_StrMode: TypeAlias = Literal["r", "w", "a", "x", "r+", "w+", "a+", "x+", "rt", "wt", "at", "xt", "r+t", "w+t", "a+t", "x+t"]
_BytesMode: TypeAlias = Literal["rb", "wb", "ab", "xb", "r+b", "w+b", "a+b", "x+b"]

if sys.version_info >= (3, 8):
    @overload
    def NamedTemporaryFile(
        mode: _StrMode,
        buffering: int = -1,
        encoding: str | None = None,
        newline: str | None = None,
        suffix: AnyStr | None = None,
        prefix: AnyStr | None = None,
        dir: GenericPath[AnyStr] | None = None,
        delete: bool = True,
        *,
        errors: str | None = None,
    ) -> _TemporaryFileWrapper[str]: ...
    @overload
    def NamedTemporaryFile(
        mode: _BytesMode = "w+b",
        buffering: int = -1,
        encoding: str | None = None,
        newline: str | None = None,
        suffix: AnyStr | None = None,
        prefix: AnyStr | None = None,
        dir: GenericPath[AnyStr] | None = None,
        delete: bool = True,
        *,
        errors: str | None = None,
    ) -> _TemporaryFileWrapper[bytes]: ...
    @overload
    def NamedTemporaryFile(
        mode: str = "w+b",
        buffering: int = -1,
        encoding: str | None = None,
        newline: str | None = None,
        suffix: AnyStr | None = None,
        prefix: AnyStr | None = None,
        dir: GenericPath[AnyStr] | None = None,
        delete: bool = True,
        *,
        errors: str | None = None,
    ) -> _TemporaryFileWrapper[Any]: ...

else:
    @overload
    def NamedTemporaryFile(
        mode: _StrMode,
        buffering: int = -1,
        encoding: str | None = None,
        newline: str | None = None,
        suffix: AnyStr | None = None,
        prefix: AnyStr | None = None,
        dir: GenericPath[AnyStr] | None = None,
        delete: bool = True,
    ) -> _TemporaryFileWrapper[str]: ...
    @overload
    def NamedTemporaryFile(
        mode: _BytesMode = "w+b",
        buffering: int = -1,
        encoding: str | None = None,
        newline: str | None = None,
        suffix: AnyStr | None = None,
        prefix: AnyStr | None = None,
        dir: GenericPath[AnyStr] | None = None,
        delete: bool = True,
    ) -> _TemporaryFileWrapper[bytes]: ...
    @overload
    def NamedTemporaryFile(
        mode: str = "w+b",
        buffering: int = -1,
        encoding: str | None = None,
        newline: str | None = None,
        suffix: AnyStr | None = None,
        prefix: AnyStr | None = None,
        dir: GenericPath[AnyStr] | None = None,
        delete: bool = True,
    ) -> _TemporaryFileWrapper[Any]: ...

if sys.platform == "win32":
    TemporaryFile = NamedTemporaryFile
else:
    if sys.version_info >= (3, 8):
        @overload
        def TemporaryFile(
            mode: _StrMode,
            buffering: int = ...,
            encoding: str | None = ...,
            newline: str | None = ...,
            suffix: AnyStr | None = ...,
            prefix: AnyStr | None = ...,
            dir: GenericPath[AnyStr] | None = ...,
            *,
            errors: str | None = ...,
        ) -> IO[str]: ...
        @overload
        def TemporaryFile(
            mode: _BytesMode = ...,
            buffering: int = ...,
            encoding: str | None = ...,
            newline: str | None = ...,
            suffix: AnyStr | None = ...,
            prefix: AnyStr | None = ...,
            dir: GenericPath[AnyStr] | None = ...,
            *,
            errors: str | None = ...,
        ) -> IO[bytes]: ...
        @overload
        def TemporaryFile(
            mode: str = ...,
            buffering: int = ...,
            encoding: str | None = ...,
            newline: str | None = ...,
            suffix: AnyStr | None = ...,
            prefix: AnyStr | None = ...,
            dir: GenericPath[AnyStr] | None = ...,
            *,
            errors: str | None = ...,
        ) -> IO[Any]: ...
    else:
        @overload
        def TemporaryFile(
            mode: _StrMode,
            buffering: int = ...,
            encoding: str | None = ...,
            newline: str | None = ...,
            suffix: AnyStr | None = ...,
            prefix: AnyStr | None = ...,
            dir: GenericPath[AnyStr] | None = ...,
        ) -> IO[str]: ...
        @overload
        def TemporaryFile(
            mode: _BytesMode = ...,
            buffering: int = ...,
            encoding: str | None = ...,
            newline: str | None = ...,
            suffix: AnyStr | None = ...,
            prefix: AnyStr | None = ...,
            dir: GenericPath[AnyStr] | None = ...,
        ) -> IO[bytes]: ...
        @overload
        def TemporaryFile(
            mode: str = ...,
            buffering: int = ...,
            encoding: str | None = ...,
            newline: str | None = ...,
            suffix: AnyStr | None = ...,
            prefix: AnyStr | None = ...,
            dir: GenericPath[AnyStr] | None = ...,
        ) -> IO[Any]: ...

class _TemporaryFileWrapper(Generic[AnyStr], IO[AnyStr]):
    file: IO[AnyStr]  # io.TextIOWrapper, io.BufferedReader or io.BufferedWriter
    name: str
    delete: bool
    def __init__(self, file: IO[AnyStr], name: str, delete: bool = True) -> None: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, exc: type[BaseException] | None, value: BaseException | None, tb: TracebackType | None) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def close(self) -> None: ...
    # These methods don't exist directly on this object, but
    # are delegated to the underlying IO object through __getattr__.
    # We need to add them here so that this class is concrete.
    def __iter__(self) -> Iterator[AnyStr]: ...
    # FIXME: __next__ doesn't actually exist on this class and should be removed:
    #        see also https://github.com/python/typeshed/pull/5456#discussion_r633068648
    # >>> import tempfile
    # >>> ntf=tempfile.NamedTemporaryFile()
    # >>> next(ntf)
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    # TypeError: '_TemporaryFileWrapper' object is not an iterator
    def __next__(self) -> AnyStr: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    def read(self, n: int = ...) -> AnyStr: ...
    def readable(self) -> bool: ...
    def readline(self, limit: int = ...) -> AnyStr: ...
    def readlines(self, hint: int = ...) -> list[AnyStr]: ...
    def seek(self, offset: int, whence: int = ...) -> int: ...
    def seekable(self) -> bool: ...
    def tell(self) -> int: ...
    def truncate(self, size: int | None = ...) -> int: ...
    def writable(self) -> bool: ...
    def write(self, s: AnyStr) -> int: ...
    def writelines(self, lines: Iterable[AnyStr]) -> None: ...

if sys.version_info >= (3, 11):
    _SpooledTemporaryFileBase = io.IOBase
else:
    _SpooledTemporaryFileBase = object

# It does not actually derive from IO[AnyStr], but it does mostly behave
# like one.
class SpooledTemporaryFile(IO[AnyStr], _SpooledTemporaryFileBase):
    @property
    def encoding(self) -> str: ...  # undocumented
    @property
    def newlines(self) -> str | tuple[str, ...] | None: ...  # undocumented
    # bytes needs to go first, as default mode is to open as bytes
    if sys.version_info >= (3, 8):
        @overload
        def __init__(
            self: SpooledTemporaryFile[bytes],
            max_size: int = 0,
            mode: _BytesMode = "w+b",
            buffering: int = -1,
            encoding: str | None = None,
            newline: str | None = None,
            suffix: str | None = None,
            prefix: str | None = None,
            dir: str | None = None,
            *,
            errors: str | None = None,
        ) -> None: ...
        @overload
        def __init__(
            self: SpooledTemporaryFile[str],
            max_size: int,
            mode: _StrMode,
            buffering: int = -1,
            encoding: str | None = None,
            newline: str | None = None,
            suffix: str | None = None,
            prefix: str | None = None,
            dir: str | None = None,
            *,
            errors: str | None = None,
        ) -> None: ...
        @overload
        def __init__(
            self: SpooledTemporaryFile[str],
            max_size: int = 0,
            *,
            mode: _StrMode,
            buffering: int = -1,
            encoding: str | None = None,
            newline: str | None = None,
            suffix: str | None = None,
            prefix: str | None = None,
            dir: str | None = None,
            errors: str | None = None,
        ) -> None: ...
        @overload
        def __init__(
            self,
            max_size: int,
            mode: str,
            buffering: int = -1,
            encoding: str | None = None,
            newline: str | None = None,
            suffix: str | None = None,
            prefix: str | None = None,
            dir: str | None = None,
            *,
            errors: str | None = None,
        ) -> None: ...
        @overload
        def __init__(
            self,
            max_size: int = 0,
            *,
            mode: str,
            buffering: int = -1,
            encoding: str | None = None,
            newline: str | None = None,
            suffix: str | None = None,
            prefix: str | None = None,
            dir: str | None = None,
            errors: str | None = None,
        ) -> None: ...
        @property
        def errors(self) -> str | None: ...
    else:
        @overload
        def __init__(
            self: SpooledTemporaryFile[bytes],
            max_size: int = 0,
            mode: _BytesMode = "w+b",
            buffering: int = -1,
            encoding: str | None = None,
            newline: str | None = None,
            suffix: str | None = None,
            prefix: str | None = None,
            dir: str | None = None,
        ) -> None: ...
        @overload
        def __init__(
            self: SpooledTemporaryFile[str],
            max_size: int,
            mode: _StrMode,
            buffering: int = -1,
            encoding: str | None = None,
            newline: str | None = None,
            suffix: str | None = None,
            prefix: str | None = None,
            dir: str | None = None,
        ) -> None: ...
        @overload
        def __init__(
            self: SpooledTemporaryFile[str],
            max_size: int = 0,
            *,
            mode: _StrMode,
            buffering: int = -1,
            encoding: str | None = None,
            newline: str | None = None,
            suffix: str | None = None,
            prefix: str | None = None,
            dir: str | None = None,
        ) -> None: ...
        @overload
        def __init__(
            self,
            max_size: int,
            mode: str,
            buffering: int = -1,
            encoding: str | None = None,
            newline: str | None = None,
            suffix: str | None = None,
            prefix: str | None = None,
            dir: str | None = None,
        ) -> None: ...
        @overload
        def __init__(
            self,
            max_size: int = 0,
            *,
            mode: str,
            buffering: int = -1,
            encoding: str | None = None,
            newline: str | None = None,
            suffix: str | None = None,
            prefix: str | None = None,
            dir: str | None = None,
        ) -> None: ...

    def rollover(self) -> None: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, exc: type[BaseException] | None, value: BaseException | None, tb: TracebackType | None) -> None: ...
    # These methods are copied from the abstract methods of IO, because
    # SpooledTemporaryFile implements IO.
    # See also https://github.com/python/typeshed/pull/2452#issuecomment-420657918.
    def close(self) -> None: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    if sys.version_info >= (3, 11):
        # These three work only if the SpooledTemporaryFile is opened in binary mode,
        # because the underlying object in text mode does not have these methods.
        def read1(self, __size: int = ...) -> AnyStr: ...
        def readinto(self, b: WriteableBuffer) -> int: ...
        def readinto1(self, b: WriteableBuffer) -> int: ...
        def detach(self) -> io.RawIOBase: ...

    def read(self, __n: int = ...) -> AnyStr: ...
    def readline(self, __limit: int | None = ...) -> AnyStr: ...  # type: ignore[override]
    def readlines(self, __hint: int = ...) -> list[AnyStr]: ...  # type: ignore[override]
    def seek(self, offset: int, whence: int = ...) -> int: ...
    def tell(self) -> int: ...
    def truncate(self, size: int | None = None) -> None: ...  # type: ignore[override]
    def write(self, s: AnyStr) -> int: ...
    def writelines(self, iterable: Iterable[AnyStr]) -> None: ...  # type: ignore[override]
    def __iter__(self) -> Iterator[AnyStr]: ...  # type: ignore[override]
    # These exist at runtime only on 3.11+.
    def readable(self) -> bool: ...
    def seekable(self) -> bool: ...
    def writable(self) -> bool: ...
    def __next__(self) -> AnyStr: ...  # type: ignore[override]
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...

class TemporaryDirectory(Generic[AnyStr]):
    name: AnyStr
    if sys.version_info >= (3, 10):
        @overload
        def __init__(
            self: TemporaryDirectory[str],
            suffix: str | None = None,
            prefix: str | None = None,
            dir: StrPath | None = None,
            ignore_cleanup_errors: bool = False,
        ) -> None: ...
        @overload
        def __init__(
            self: TemporaryDirectory[bytes],
            suffix: bytes | None = None,
            prefix: bytes | None = None,
            dir: BytesPath | None = None,
            ignore_cleanup_errors: bool = False,
        ) -> None: ...
    else:
        @overload
        def __init__(
            self: TemporaryDirectory[str], suffix: str | None = None, prefix: str | None = None, dir: StrPath | None = None
        ) -> None: ...
        @overload
        def __init__(
            self: TemporaryDirectory[bytes],
            suffix: bytes | None = None,
            prefix: bytes | None = None,
            dir: BytesPath | None = None,
        ) -> None: ...

    def cleanup(self) -> None: ...
    def __enter__(self) -> AnyStr: ...
    def __exit__(self, exc: type[BaseException] | None, value: BaseException | None, tb: TracebackType | None) -> None: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...

# The overloads overlap, but they should still work fine.
@overload
def mkstemp(  # type: ignore[misc]
    suffix: str | None = None, prefix: str | None = None, dir: StrPath | None = None, text: bool = False
) -> tuple[int, str]: ...
@overload
def mkstemp(
    suffix: bytes | None = None, prefix: bytes | None = None, dir: BytesPath | None = None, text: bool = False
) -> tuple[int, bytes]: ...

# The overloads overlap, but they should still work fine.
@overload
def mkdtemp(suffix: str | None = None, prefix: str | None = None, dir: StrPath | None = None) -> str: ...  # type: ignore[misc]
@overload
def mkdtemp(suffix: bytes | None = None, prefix: bytes | None = None, dir: BytesPath | None = None) -> bytes: ...
def mktemp(suffix: str = "", prefix: str = "tmp", dir: StrPath | None = None) -> str: ...
def gettempdirb() -> bytes: ...
def gettempprefixb() -> bytes: ...
def gettempdir() -> str: ...
def gettempprefix() -> str: ...
