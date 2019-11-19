"""An implementation of Decimal as a DType.

https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionDtype.html#pandas.api.extensions.ExtensionDtype
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionArray.html#pandas.api.extensions.ExtensionArray

https://github.com/pandas-dev/pandas/tree/e246c3b05924ac1fe083565a765ce847fcad3d91/pandas/tests/extension/decimal

"""

import decimal
import numpy as np

from pandas.core.arrays import ExtensionArray
from pandas.core.dtypes.base import ExtensionDtype


class DecimalDtype(ExtensionDtype):
    """A custom data type, to be paired with an ExtensionArray."""

    type = decimal.Decimal
    name = "decimal"
    na_value = decimal.Decimal("NaN")

    @classmethod
    def construct_array_type(cls):
        """Return the array type associated with this dtype."""
        return DecimalArray


class DecimalArray(ExtensionArray):
    """Abstract base class for custom 1-D array types."""

    def __init__(self, values, dtype=None, copy=False):
        """Instantiate the array.

        If you're doing any type coercion in here, you will also need
        that in an overwritten __settiem__ method.

        But, here we coerce the input values into Decimals.
        """
        values = [decimal.Decimal(val) for val in values]
        self._data = np.asarray(values, dtype=object)
        self._dtype = DecimalDtype()

    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        """Construct a new ExtensionArray from a sequence of scalars."""
        return cls(scalars, dtype=dtype)

    @classmethod
    def _from_factorized(cls, values, original):
        """Reconstruct an ExtensionArray after factorization."""
        return cls(values)

    def __getitem__(self, item):
        """Select a subset of self."""
        return self._data[item]

    def __len__(self) -> int:
        """Length of this array."""
        return len(self._data)

    @property
    def nbytes(self):
        """The byte size of the data."""
        return self._itemsize * len(self)

    @property
    def dtype(self):
        """An instance of 'ExtensionDtype'."""
        return self._dtype

    def isna(self):
        """A 1-D array indicating if each value is missing."""
        return np.array([x.is_nan() for x in self._data], dtype=bool)

    def take(self, indexer, allow_fill=False, fill_value=None):
        """Take elements from an array.

        Relies on the take method defined in pandas:
        https://github.com/pandas-dev/pandas/blob/e246c3b05924ac1fe083565a765ce847fcad3d91/pandas/core/algorithms.py#L1483
        """
        from pandas.api.extensions import take

        data = self._data
        if allow_fill and fill_value is None:
            fill_value = self.dtype.na_value

        result = take(
            data, indexer, fill_value=fill_value, allow_fill=allow_fill)
        return self._from_sequence(result)

    def copy(self):
        """Return a copy of the array."""
        return type(self)(self._data.copy())

    @classmethod
    def _concat_same_type(cls, to_concat):
        """Concatenate multiple arrays."""
        return cls(np.concatenate([x._data for x in to_concat]))
