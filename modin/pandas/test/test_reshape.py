import pandas
import pytest
import numpy as np
import modin.pandas as pd

from .utils import df_equals, test_data_values


def test_get_dummies():
    s = pd.Series(list("abca"))
    with pytest.warns(UserWarning):
        pd.get_dummies(s)

    s1 = ["a", "b", np.nan]
    with pytest.warns(UserWarning):
        pd.get_dummies(s1)

    with pytest.warns(UserWarning):
        pd.get_dummies(s1, dummy_na=True)

    data = {"A": ["a", "b", "a"], "B": ["b", "a", "c"], "C": [1, 2, 3]}
    modin_df = pd.DataFrame(data)
    pandas_df = pandas.DataFrame(data)

    modin_result = pd.get_dummies(modin_df, prefix=["col1", "col2"])
    pandas_result = pandas.get_dummies(pandas_df, prefix=["col1", "col2"])
    df_equals(modin_result, pandas_result)

    modin_result = pd.get_dummies(pd.DataFrame(pd.Series(list("abcdeabac"))))
    pandas_result = pandas.get_dummies(
        pandas.DataFrame(pandas.Series(list("abcdeabac")))
    )
    df_equals(modin_result, pandas_result)

    with pytest.raises(NotImplementedError):
        pd.get_dummies(modin_df, prefix=["col1", "col2"], sparse=True)

    with pytest.warns(UserWarning):
        pd.get_dummies(pd.Series(list("abcaa")))

    with pytest.warns(UserWarning):
        pd.get_dummies(pd.Series(list("abcaa")), drop_first=True)

    with pytest.warns(UserWarning):
        pd.get_dummies(pd.Series(list("abc")), dtype=float)

    with pytest.warns(UserWarning):
        pd.get_dummies(1)


def test_melt():
    data = test_data_values[0]
    with pytest.warns(UserWarning):
        pd.melt(pd.DataFrame(data))


def test_crosstab():
    a = np.array(
        ["foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar", "foo", "foo", "foo"],
        dtype=object,
    )
    b = np.array(
        ["one", "one", "one", "two", "one", "one", "one", "two", "two", "two", "one"],
        dtype=object,
    )
    c = np.array(
        [
            "dull",
            "dull",
            "shiny",
            "dull",
            "dull",
            "shiny",
            "shiny",
            "dull",
            "shiny",
            "shiny",
            "shiny",
        ],
        dtype=object,
    )

    with pytest.warns(UserWarning):
        df = pd.crosstab(a, [b, c], rownames=["a"], colnames=["b", "c"])
        assert isinstance(df, pd.DataFrame)

    foo = pd.Categorical(["a", "b"], categories=["a", "b", "c"])
    bar = pd.Categorical(["d", "e"], categories=["d", "e", "f"])

    with pytest.warns(UserWarning):
        df = pd.crosstab(foo, bar)
        assert isinstance(df, pd.DataFrame)

    with pytest.warns(UserWarning):
        df = pd.crosstab(foo, bar, dropna=False)
        assert isinstance(df, pd.DataFrame)


def test_lreshape():
    data = pd.DataFrame(
        {
            "hr1": [514, 573],
            "hr2": [545, 526],
            "team": ["Red Sox", "Yankees"],
            "year1": [2007, 2008],
            "year2": [2008, 2008],
        }
    )

    with pytest.warns(UserWarning):
        df = pd.lreshape(data, {"year": ["year1", "year2"], "hr": ["hr1", "hr2"]})
        assert isinstance(df, pd.DataFrame)

    with pytest.raises(ValueError):
        pd.lreshape(data.to_numpy(), {"year": ["year1", "year2"], "hr": ["hr1", "hr2"]})


def test_wide_to_long():
    data = pd.DataFrame(
        {
            "hr1": [514, 573],
            "hr2": [545, 526],
            "team": ["Red Sox", "Yankees"],
            "year1": [2007, 2008],
            "year2": [2008, 2008],
        }
    )

    with pytest.warns(UserWarning):
        df = pd.wide_to_long(data, ["hr", "year"], "team", "index")
        assert isinstance(df, pd.DataFrame)

    with pytest.raises(ValueError):
        pd.wide_to_long(data.to_numpy(), ["hr", "year"], "team", "index")
