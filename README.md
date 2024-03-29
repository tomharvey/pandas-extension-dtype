# Basic use of the ExtensionArray and ExtensionDtype

A pandas Series (or DataFrame) can contain data in one of only a few types.
As of version 0.25, we can define custom types and use these.

The [cyberpandas](https://github.com/ContinuumIO/cyberpandas/) project uses
this approach to allow for IP and MAC Addresses to be used with a richer
and faster interface than if just using String representations of these
networking values.

It also created the impetus for the creation of the extension system,
widely discussed in [this Pull Request on the pandas
project](https://github.com/pandas-dev/pandas/pull/19268/)

See [this story](https://tomaugspurger.github.io/pandas-extension-arrays.html)
for more on how this came to pass.

### Using these extensions

The pandas docs outline the methods which must be implemented in the
[ExtensionDtype](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionDtype.html#pandas.api.extensions.ExtensionDtype)
and [ExtensionArray](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionArray.html#pandas.api.extensions.ExtensionArray)
classes when creating your own custom data types.

But there isn't much in the way of a minimum working example.

The [test suite for Pandas has an implementation for storing Decimals](https://github.com/pandas-dev/pandas/tree/e246c3b05924ac1fe083565a765ce847fcad3d91/pandas/tests/extension/decimal)
, and is a great usage guide to these new extension classes.

[Here](https://github.com/tomharvey/pandas-extension-dtype/blob/master/decimal_array.py)
, in the `decimal_array` file, is the miminum working implementation of that.
It's lifted from the Test Suite in pandas and stripped of much of the mathematical functionality,
but it helped me understand how to use these classes in building my own custom dtypes.

While it lacks the ability to make much use of the Decimal objects 
(See the full test suite for a more full implementation of usable Decimal), it
provides a working implementation to build your custom data type from.


### Example

While you can always create a `Series` of floats in pandas:

``` python
>>> float_series = pd.Series([0.1, 0.2, 0.3])
>>> print(float_series)
0    0.1
1    0.2
2    0.3
dtype: float64

```

**Note** the dtype is `float64`

With the classes in here you can create a series of Decimals:

```python
>>> decimal_series = pd.Series(DecimalArray([0.1, 0.2, 0.3]))
>>> print(decimal_series)
0    0.10000000000000000555111512312578270211815834...
1    0.20000000000000001110223024625156540423631668...
2    0.29999999999999998889776975374843459576368331...
dtype: decimal
```

Which now holds the data as an array of largely useless `Decimal` objects! Success!
