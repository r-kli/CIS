from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Literal
from typing import Sequence

from narwhals._expression_parsing import reuse_series_implementation
from narwhals._expression_parsing import reuse_series_namespace_implementation
from narwhals.dependencies import get_numpy
from narwhals.dependencies import is_numpy_array
from narwhals.exceptions import ColumnNotFoundError
from narwhals.utils import Implementation

if TYPE_CHECKING:
    from typing_extensions import Self

    from narwhals._arrow.dataframe import ArrowDataFrame
    from narwhals._arrow.namespace import ArrowNamespace
    from narwhals._arrow.series import ArrowSeries
    from narwhals._arrow.typing import IntoArrowExpr
    from narwhals.dtypes import DType
    from narwhals.utils import Version


class ArrowExpr:
    _implementation: Implementation = Implementation.PYARROW

    def __init__(
        self: Self,
        call: Callable[[ArrowDataFrame], list[ArrowSeries]],
        *,
        depth: int,
        function_name: str,
        root_names: list[str] | None,
        output_names: list[str] | None,
        backend_version: tuple[int, ...],
        version: Version,
    ) -> None:
        self._call = call
        self._depth = depth
        self._function_name = function_name
        self._root_names = root_names
        self._depth = depth
        self._output_names = output_names
        self._implementation = Implementation.PYARROW
        self._backend_version = backend_version
        self._version = version

    def __repr__(self: Self) -> str:  # pragma: no cover
        return (
            f"ArrowExpr("
            f"depth={self._depth}, "
            f"function_name={self._function_name}, "
            f"root_names={self._root_names}, "
            f"output_names={self._output_names}"
        )

    @classmethod
    def from_column_names(
        cls: type[Self],
        *column_names: str,
        backend_version: tuple[int, ...],
        version: Version,
    ) -> Self:
        from narwhals._arrow.series import ArrowSeries

        def func(df: ArrowDataFrame) -> list[ArrowSeries]:
            try:
                return [
                    ArrowSeries(
                        df._native_frame[column_name],
                        name=column_name,
                        backend_version=df._backend_version,
                        version=df._version,
                    )
                    for column_name in column_names
                ]
            except KeyError as e:
                missing_columns = [x for x in column_names if x not in df.columns]
                raise ColumnNotFoundError.from_missing_and_available_column_names(
                    missing_columns=missing_columns,
                    available_columns=df.columns,
                ) from e

        return cls(
            func,
            depth=0,
            function_name="col",
            root_names=list(column_names),
            output_names=list(column_names),
            backend_version=backend_version,
            version=version,
        )

    @classmethod
    def from_column_indices(
        cls: type[Self],
        *column_indices: int,
        backend_version: tuple[int, ...],
        version: Version,
    ) -> Self:
        from narwhals._arrow.series import ArrowSeries

        def func(df: ArrowDataFrame) -> list[ArrowSeries]:
            return [
                ArrowSeries(
                    df._native_frame[column_index],
                    name=df._native_frame.column_names[column_index],
                    backend_version=df._backend_version,
                    version=df._version,
                )
                for column_index in column_indices
            ]

        return cls(
            func,
            depth=0,
            function_name="nth",
            root_names=None,
            output_names=None,
            backend_version=backend_version,
            version=version,
        )

    def __narwhals_namespace__(self: Self) -> ArrowNamespace:
        from narwhals._arrow.namespace import ArrowNamespace

        return ArrowNamespace(
            backend_version=self._backend_version, version=self._version
        )

    def __narwhals_expr__(self: Self) -> None: ...

    def __eq__(self: Self, other: ArrowExpr | Any) -> Self:  # type: ignore[override]
        return reuse_series_implementation(self, "__eq__", other=other)

    def __ne__(self: Self, other: ArrowExpr | Any) -> Self:  # type: ignore[override]
        return reuse_series_implementation(self, "__ne__", other=other)

    def __ge__(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "__ge__", other=other)

    def __gt__(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "__gt__", other=other)

    def __le__(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "__le__", other=other)

    def __lt__(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "__lt__", other=other)

    def __and__(self: Self, other: ArrowExpr | bool | Any) -> Self:
        return reuse_series_implementation(self, "__and__", other=other)

    def __rand__(self: Self, other: ArrowExpr | bool | Any) -> Self:
        other = self.__narwhals_namespace__().lit(other, dtype=None)
        return other.__and__(self)  # type: ignore[return-value]

    def __or__(self: Self, other: ArrowExpr | bool | Any) -> Self:
        return reuse_series_implementation(self, "__or__", other=other)

    def __ror__(self: Self, other: ArrowExpr | bool | Any) -> Self:
        other = self.__narwhals_namespace__().lit(other, dtype=None)
        return other.__or__(self)  # type: ignore[return-value]

    def __add__(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "__add__", other)

    def __radd__(self: Self, other: ArrowExpr | Any) -> Self:
        other = self.__narwhals_namespace__().lit(other, dtype=None)
        return other.__add__(self)  # type: ignore[return-value]

    def __sub__(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "__sub__", other)

    def __rsub__(self: Self, other: ArrowExpr | Any) -> Self:
        other = self.__narwhals_namespace__().lit(other, dtype=None)
        return other.__sub__(self)  # type: ignore[return-value]

    def __mul__(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "__mul__", other)

    def __rmul__(self: Self, other: ArrowExpr | Any) -> Self:
        other = self.__narwhals_namespace__().lit(other, dtype=None)
        return other.__mul__(self)  # type: ignore[return-value]

    def __pow__(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "__pow__", other)

    def __rpow__(self: Self, other: ArrowExpr | Any) -> Self:
        other = self.__narwhals_namespace__().lit(other, dtype=None)
        return other.__pow__(self)  # type: ignore[return-value]

    def __floordiv__(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "__floordiv__", other)

    def __rfloordiv__(self: Self, other: ArrowExpr | Any) -> Self:
        other = self.__narwhals_namespace__().lit(other, dtype=None)
        return other.__floordiv__(self)  # type: ignore[return-value]

    def __truediv__(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "__truediv__", other)

    def __rtruediv__(self: Self, other: ArrowExpr | Any) -> Self:
        other = self.__narwhals_namespace__().lit(other, dtype=None)
        return other.__truediv__(self)  # type: ignore[return-value]

    def __mod__(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "__mod__", other)

    def __rmod__(self: Self, other: ArrowExpr | Any) -> Self:
        other = self.__narwhals_namespace__().lit(other, dtype=None)
        return other.__mod__(self)  # type: ignore[return-value]

    def __invert__(self: Self) -> Self:
        return reuse_series_implementation(self, "__invert__")

    def len(self: Self) -> Self:
        return reuse_series_implementation(self, "len", returns_scalar=True)

    def filter(self: Self, *predicates: IntoArrowExpr) -> Self:
        plx = self.__narwhals_namespace__()
        expr = plx.all_horizontal(*predicates)
        return reuse_series_implementation(self, "filter", other=expr)

    def mean(self: Self) -> Self:
        return reuse_series_implementation(self, "mean", returns_scalar=True)

    def median(self: Self) -> Self:
        return reuse_series_implementation(self, "median", returns_scalar=True)

    def count(self: Self) -> Self:
        return reuse_series_implementation(self, "count", returns_scalar=True)

    def n_unique(self: Self) -> Self:
        return reuse_series_implementation(self, "n_unique", returns_scalar=True)

    def std(self: Self, ddof: int = 1) -> Self:
        return reuse_series_implementation(self, "std", ddof=ddof, returns_scalar=True)

    def skew(self: Self) -> Self:
        return reuse_series_implementation(self, "skew", returns_scalar=True)

    def cast(self: Self, dtype: DType) -> Self:
        return reuse_series_implementation(self, "cast", dtype)

    def abs(self: Self) -> Self:
        return reuse_series_implementation(self, "abs")

    def diff(self: Self) -> Self:
        return reuse_series_implementation(self, "diff")

    def cum_sum(self: Self, *, reverse: bool) -> Self:
        return reuse_series_implementation(self, "cum_sum", reverse=reverse)

    def round(self: Self, decimals: int) -> Self:
        return reuse_series_implementation(self, "round", decimals)

    def any(self: Self) -> Self:
        return reuse_series_implementation(self, "any", returns_scalar=True)

    def min(self: Self) -> Self:
        return reuse_series_implementation(self, "min", returns_scalar=True)

    def max(self: Self) -> Self:
        return reuse_series_implementation(self, "max", returns_scalar=True)

    def all(self: Self) -> Self:
        return reuse_series_implementation(self, "all", returns_scalar=True)

    def sum(self: Self) -> Self:
        return reuse_series_implementation(self, "sum", returns_scalar=True)

    def drop_nulls(self: Self) -> Self:
        return reuse_series_implementation(self, "drop_nulls")

    def shift(self: Self, n: int) -> Self:
        return reuse_series_implementation(self, "shift", n)

    def alias(self: Self, name: str) -> Self:
        # Define this one manually, so that we can
        # override `output_names` and not increase depth
        return self.__class__(
            lambda df: [series.alias(name) for series in self._call(df)],
            depth=self._depth,
            function_name=self._function_name,
            root_names=self._root_names,
            output_names=[name],
            backend_version=self._backend_version,
            version=self._version,
        )

    def null_count(self: Self) -> Self:
        return reuse_series_implementation(self, "null_count", returns_scalar=True)

    def is_null(self: Self) -> Self:
        return reuse_series_implementation(self, "is_null")

    def is_between(self: Self, lower_bound: Any, upper_bound: Any, closed: str) -> Self:
        return reuse_series_implementation(
            self, "is_between", lower_bound, upper_bound, closed
        )

    def head(self: Self, n: int) -> Self:
        return reuse_series_implementation(self, "head", n)

    def tail(self: Self, n: int) -> Self:
        return reuse_series_implementation(self, "tail", n)

    def is_in(self: Self, other: ArrowExpr | Any) -> Self:
        return reuse_series_implementation(self, "is_in", other)

    def arg_true(self: Self) -> Self:
        return reuse_series_implementation(self, "arg_true")

    def sample(
        self: Self,
        n: int | None,
        *,
        fraction: float | None,
        with_replacement: bool,
        seed: int | None,
    ) -> Self:
        return reuse_series_implementation(
            self,
            "sample",
            n=n,
            fraction=fraction,
            with_replacement=with_replacement,
            seed=seed,
        )

    def fill_null(
        self: Self,
        value: Any | None,
        strategy: Literal["forward", "backward"] | None,
        limit: int | None,
    ) -> Self:
        return reuse_series_implementation(
            self, "fill_null", value=value, strategy=strategy, limit=limit
        )

    def is_duplicated(self: Self) -> Self:
        return reuse_series_implementation(self, "is_duplicated")

    def is_unique(self: Self) -> Self:
        return reuse_series_implementation(self, "is_unique")

    def is_first_distinct(self: Self) -> Self:
        return reuse_series_implementation(self, "is_first_distinct")

    def is_last_distinct(self: Self) -> Self:
        return reuse_series_implementation(self, "is_last_distinct")

    def unique(self: Self, *, maintain_order: bool) -> Self:
        return reuse_series_implementation(self, "unique", maintain_order=maintain_order)

    def replace_strict(
        self: Self, old: Sequence[Any], new: Sequence[Any], *, return_dtype: DType | None
    ) -> Self:
        return reuse_series_implementation(
            self, "replace_strict", old, new, return_dtype=return_dtype
        )

    def sort(self: Self, *, descending: bool, nulls_last: bool) -> Self:
        return reuse_series_implementation(
            self, "sort", descending=descending, nulls_last=nulls_last
        )

    def quantile(
        self: Self,
        quantile: float,
        interpolation: Literal["nearest", "higher", "lower", "midpoint", "linear"],
    ) -> Self:
        return reuse_series_implementation(
            self, "quantile", quantile, interpolation, returns_scalar=True
        )

    def gather_every(self: Self, n: int, offset: int = 0) -> Self:
        return reuse_series_implementation(self, "gather_every", n=n, offset=offset)

    def clip(self: Self, lower_bound: Any | None, upper_bound: Any | None) -> Self:
        return reuse_series_implementation(
            self, "clip", lower_bound=lower_bound, upper_bound=upper_bound
        )

    def over(self: Self, keys: list[str]) -> Self:
        def func(df: ArrowDataFrame) -> list[ArrowSeries]:
            if self._output_names is None:
                msg = (
                    "Anonymous expressions are not supported in over.\n"
                    "Instead of `nw.all()`, try using a named expression, such as "
                    "`nw.col('a', 'b')`\n"
                )
                raise ValueError(msg)
            tmp = df.group_by(*keys, drop_null_keys=False).agg(self)
            tmp = df.select(*keys).join(
                tmp, how="left", left_on=keys, right_on=keys, suffix="_right"
            )
            return [tmp[name] for name in self._output_names]

        return self.__class__(
            func,
            depth=self._depth + 1,
            function_name=self._function_name + "->over",
            root_names=self._root_names,
            output_names=self._output_names,
            backend_version=self._backend_version,
            version=self._version,
        )

    def mode(self: Self) -> Self:
        return reuse_series_implementation(self, "mode")

    def map_batches(
        self: Self,
        function: Callable[[Any], Any],
        return_dtype: DType | None,
    ) -> Self:
        def func(df: ArrowDataFrame) -> list[ArrowSeries]:
            input_series_list = self._call(df)
            output_names = [input_series.name for input_series in input_series_list]
            result = [function(series) for series in input_series_list]

            if is_numpy_array(result[0]):
                result = [
                    df.__narwhals_namespace__()
                    ._create_compliant_series(array)
                    .alias(output_name)
                    for array, output_name in zip(result, output_names)
                ]
            elif (np := get_numpy()) is not None and np.isscalar(result[0]):
                result = [
                    df.__narwhals_namespace__()
                    ._create_compliant_series([array])
                    .alias(output_name)
                    for array, output_name in zip(result, output_names)
                ]
            if return_dtype is not None:
                result = [series.cast(return_dtype) for series in result]
            return result

        return self.__class__(
            func,
            depth=self._depth + 1,
            function_name=self._function_name + "->map_batches",
            root_names=self._root_names,
            output_names=self._output_names,
            backend_version=self._backend_version,
            version=self._version,
        )

    def is_finite(self: Self) -> Self:
        return reuse_series_implementation(self, "is_finite")

    def cum_count(self: Self, *, reverse: bool) -> Self:
        return reuse_series_implementation(self, "cum_count", reverse=reverse)

    def cum_min(self: Self, *, reverse: bool) -> Self:
        return reuse_series_implementation(self, "cum_min", reverse=reverse)

    def cum_max(self: Self, *, reverse: bool) -> Self:
        return reuse_series_implementation(self, "cum_max", reverse=reverse)

    def cum_prod(self: Self, *, reverse: bool) -> Self:
        return reuse_series_implementation(self, "cum_prod", reverse=reverse)

    def rolling_sum(
        self: Self,
        window_size: int,
        *,
        min_periods: int | None,
        center: bool,
    ) -> Self:
        return reuse_series_implementation(
            self,
            "rolling_sum",
            window_size=window_size,
            min_periods=min_periods,
            center=center,
        )

    def rolling_mean(
        self: Self,
        window_size: int,
        *,
        min_periods: int | None,
        center: bool,
    ) -> Self:
        return reuse_series_implementation(
            self,
            "rolling_mean",
            window_size=window_size,
            min_periods=min_periods,
            center=center,
        )

    @property
    def dt(self: Self) -> ArrowExprDateTimeNamespace:
        return ArrowExprDateTimeNamespace(self)

    @property
    def str(self: Self) -> ArrowExprStringNamespace:
        return ArrowExprStringNamespace(self)

    @property
    def cat(self: Self) -> ArrowExprCatNamespace:
        return ArrowExprCatNamespace(self)

    @property
    def name(self: Self) -> ArrowExprNameNamespace:
        return ArrowExprNameNamespace(self)

    @property
    def list(self: Self) -> ArrowExprListNamespace:
        return ArrowExprListNamespace(self)


class ArrowExprCatNamespace:
    def __init__(self: Self, expr: ArrowExpr) -> None:
        self._compliant_expr = expr

    def get_categories(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr,
            "cat",
            "get_categories",
        )


class ArrowExprDateTimeNamespace:
    def __init__(self: Self, expr: ArrowExpr) -> None:
        self._compliant_expr = expr

    def to_string(self: Self, format: str) -> ArrowExpr:  # noqa: A002
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "to_string", format
        )

    def replace_time_zone(self: Self, time_zone: str | None) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "replace_time_zone", time_zone
        )

    def convert_time_zone(self: Self, time_zone: str) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "convert_time_zone", time_zone
        )

    def timestamp(self: Self, time_unit: Literal["ns", "us", "ms"] = "us") -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "timestamp", time_unit
        )

    def date(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(self._compliant_expr, "dt", "date")

    def year(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(self._compliant_expr, "dt", "year")

    def month(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(self._compliant_expr, "dt", "month")

    def day(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(self._compliant_expr, "dt", "day")

    def hour(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(self._compliant_expr, "dt", "hour")

    def minute(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(self._compliant_expr, "dt", "minute")

    def second(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(self._compliant_expr, "dt", "second")

    def millisecond(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "millisecond"
        )

    def microsecond(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "microsecond"
        )

    def nanosecond(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "nanosecond"
        )

    def ordinal_day(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "ordinal_day"
        )

    def total_minutes(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "total_minutes"
        )

    def total_seconds(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "total_seconds"
        )

    def total_milliseconds(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "total_milliseconds"
        )

    def total_microseconds(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "total_microseconds"
        )

    def total_nanoseconds(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "dt", "total_nanoseconds"
        )


class ArrowExprStringNamespace:
    def __init__(self: Self, expr: ArrowExpr) -> None:
        self._compliant_expr = expr

    def len_chars(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "str", "len_chars"
        )

    def replace(
        self: Self,
        pattern: str,
        value: str,
        *,
        literal: bool,
        n: int,
    ) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr,
            "str",
            "replace",
            pattern,
            value,
            literal=literal,
            n=n,
        )

    def replace_all(
        self: Self,
        pattern: str,
        value: str,
        *,
        literal: bool,
    ) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr,
            "str",
            "replace_all",
            pattern,
            value,
            literal=literal,
        )

    def strip_chars(self: Self, characters: str | None) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr,
            "str",
            "strip_chars",
            characters,
        )

    def starts_with(self: Self, prefix: str) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr,
            "str",
            "starts_with",
            prefix,
        )

    def ends_with(self: Self, suffix: str) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr,
            "str",
            "ends_with",
            suffix,
        )

    def contains(self, pattern: str, *, literal: bool) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "str", "contains", pattern, literal=literal
        )

    def slice(self: Self, offset: int, length: int | None) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr, "str", "slice", offset, length
        )

    def to_datetime(self: Self, format: str | None) -> ArrowExpr:  # noqa: A002
        return reuse_series_namespace_implementation(
            self._compliant_expr,
            "str",
            "to_datetime",
            format,
        )

    def to_uppercase(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr,
            "str",
            "to_uppercase",
        )

    def to_lowercase(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._compliant_expr,
            "str",
            "to_lowercase",
        )


class ArrowExprNameNamespace:
    def __init__(self: Self, expr: ArrowExpr) -> None:
        self._compliant_expr = expr

    def keep(self: Self) -> ArrowExpr:
        root_names = self._compliant_expr._root_names

        if root_names is None:
            msg = (
                "Anonymous expressions are not supported in `.name.keep`.\n"
                "Instead of `nw.all()`, try using a named expression, such as "
                "`nw.col('a', 'b')`\n"
            )
            raise ValueError(msg)

        return self._compliant_expr.__class__(
            lambda df: [
                series.alias(name)
                for series, name in zip(self._compliant_expr._call(df), root_names)
            ],
            depth=self._compliant_expr._depth,
            function_name=self._compliant_expr._function_name,
            root_names=root_names,
            output_names=root_names,
            backend_version=self._compliant_expr._backend_version,
            version=self._compliant_expr._version,
        )

    def map(self: Self, function: Callable[[str], str]) -> ArrowExpr:
        root_names = self._compliant_expr._root_names

        if root_names is None:
            msg = (
                "Anonymous expressions are not supported in `.name.map`.\n"
                "Instead of `nw.all()`, try using a named expression, such as "
                "`nw.col('a', 'b')`\n"
            )
            raise ValueError(msg)

        output_names = [function(str(name)) for name in root_names]

        return self._compliant_expr.__class__(
            lambda df: [
                series.alias(name)
                for series, name in zip(self._compliant_expr._call(df), output_names)
            ],
            depth=self._compliant_expr._depth,
            function_name=self._compliant_expr._function_name,
            root_names=root_names,
            output_names=output_names,
            backend_version=self._compliant_expr._backend_version,
            version=self._compliant_expr._version,
        )

    def prefix(self: Self, prefix: str) -> ArrowExpr:
        root_names = self._compliant_expr._root_names
        if root_names is None:
            msg = (
                "Anonymous expressions are not supported in `.name.prefix`.\n"
                "Instead of `nw.all()`, try using a named expression, such as "
                "`nw.col('a', 'b')`\n"
            )
            raise ValueError(msg)

        output_names = [prefix + str(name) for name in root_names]
        return self._compliant_expr.__class__(
            lambda df: [
                series.alias(name)
                for series, name in zip(self._compliant_expr._call(df), output_names)
            ],
            depth=self._compliant_expr._depth,
            function_name=self._compliant_expr._function_name,
            root_names=root_names,
            output_names=output_names,
            backend_version=self._compliant_expr._backend_version,
            version=self._compliant_expr._version,
        )

    def suffix(self: Self, suffix: str) -> ArrowExpr:
        root_names = self._compliant_expr._root_names
        if root_names is None:
            msg = (
                "Anonymous expressions are not supported in `.name.suffix`.\n"
                "Instead of `nw.all()`, try using a named expression, such as "
                "`nw.col('a', 'b')`\n"
            )
            raise ValueError(msg)

        output_names = [str(name) + suffix for name in root_names]

        return self._compliant_expr.__class__(
            lambda df: [
                series.alias(name)
                for series, name in zip(self._compliant_expr._call(df), output_names)
            ],
            depth=self._compliant_expr._depth,
            function_name=self._compliant_expr._function_name,
            root_names=root_names,
            output_names=output_names,
            backend_version=self._compliant_expr._backend_version,
            version=self._compliant_expr._version,
        )

    def to_lowercase(self: Self) -> ArrowExpr:
        root_names = self._compliant_expr._root_names

        if root_names is None:
            msg = (
                "Anonymous expressions are not supported in `.name.to_lowercase`.\n"
                "Instead of `nw.all()`, try using a named expression, such as "
                "`nw.col('a', 'b')`\n"
            )
            raise ValueError(msg)
        output_names = [str(name).lower() for name in root_names]

        return self._compliant_expr.__class__(
            lambda df: [
                series.alias(name)
                for series, name in zip(self._compliant_expr._call(df), output_names)
            ],
            depth=self._compliant_expr._depth,
            function_name=self._compliant_expr._function_name,
            root_names=root_names,
            output_names=output_names,
            backend_version=self._compliant_expr._backend_version,
            version=self._compliant_expr._version,
        )

    def to_uppercase(self: Self) -> ArrowExpr:
        root_names = self._compliant_expr._root_names

        if root_names is None:
            msg = (
                "Anonymous expressions are not supported in `.name.to_uppercase`.\n"
                "Instead of `nw.all()`, try using a named expression, such as "
                "`nw.col('a', 'b')`\n"
            )
            raise ValueError(msg)
        output_names = [str(name).upper() for name in root_names]

        return self._compliant_expr.__class__(
            lambda df: [
                series.alias(name)
                for series, name in zip(self._compliant_expr._call(df), output_names)
            ],
            depth=self._compliant_expr._depth,
            function_name=self._compliant_expr._function_name,
            root_names=root_names,
            output_names=output_names,
            backend_version=self._compliant_expr._backend_version,
            version=self._compliant_expr._version,
        )


class ArrowExprListNamespace:
    def __init__(self: Self, expr: ArrowExpr) -> None:
        self._expr = expr

    def len(self: Self) -> ArrowExpr:
        return reuse_series_namespace_implementation(
            self._expr,
            "list",
            "len",
        )