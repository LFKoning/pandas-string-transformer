"""
Module with the StringTransformer class for chaining string related operations.
The transformer operates on Pandas data frame columns of the object data type.
A subset of the columns can be supplied via the construtor.

Example
-------
# Transformer stripping white-space and converting to lower case.
tfm = StringTransformer()
tfm.add(str.strip)
tfm.add(str.lower)

# Same but shorter
tfm = StringTransformer()
tfm + str.strip + str.lower

# Transform a dataframe
# Note: Only column `lab` will be transformed due to data type selection.
df = pd.DataFrame({"x": [1, 2, 3], "label": [" One ", " Two ", " Three "]})
tfm.transform(df)
"""

class StringTransformer:
    """
    StringTransformer class for chaining string operations.

    Parameters
    ----------
    columns : list[str], optional
        Custom selection of column names.
    """

    def __init__(self, columns=None):
        self._columns = columns
        self._pipeline = []

    def add(self, func, *args, **kwargs):
        """
        Adds handler function to the transformation pipeline.

        Parameters
        ----------
        func : Callable
            Callable function that processes a string value.
        args : mixed
            Positional arguments for the callable function.
        kwargs : mixed
            Keyworded arguments for the callable function.
        """
        self._check_function(func)
        self._pipeline.append((func, args, kwargs))

    def __add__(self, step):
        """
        Adds handler to the processing pipeline.

        Parameters
        ----------
        step : Union[callable, tuple]
            Processing step to add, either callable or tuple.
            In case of a tuple, the following elements can be present:
            - callable: assumed to be the string processing function.
            - tuple / list: assumed to be the positional arguments to the callable.
            - dict: assumed to be the keyworden arguments to the callable.

        Returns
        -------
        StringTransformer
            Returns self for chaining additional steps.
        """
        func = None
        args = []
        kwargs = {}

        # Step definition only has name element
        if callable(step):
            func = step

        # Get elements from the step definition
        elif isinstance(step, tuple):
            for elem in step:
                if callable(elem):
                    func = elem
                elif isinstance(elem, dict):
                    kwargs = elem
                elif isinstance(elem, (tuple, list)):
                    args = elem

        else:
            raise TypeError("Can only add steps as callable or tuple.")

        # Add the step if we have at least a callable function
        if not func:
            raise ValueError("No handler name specified.")

        self.add(func, *args, **kwargs)

        # Return self for chaining additions
        return self

    @staticmethod
    def _check_function(func, *args, **kwargs):
        """
        Checks function for transforming strings.

        Parameters
        ----------
        func : Callable
            Callable function that processes a string value.
        args : mixed
            Positional arguments for the callable function.
        kwargs : mixed
            Keyworded arguments for the callable function.
        """
        if not callable(func):
            raise TypeError("Supplied function is not callable!")
        try:
            result = func("test_string", *args, **kwargs)
        except Exception:
            raise ValueError("Supplied function does not work with strings!")

        if not isinstance(result, str):
            raise ValueError("Supplied function does not return a string!")

    def list_steps(self):
        """Returns the transfomation pipeline."""
        return self._pipeline


    def fit(self, X, y=None):
        """Stateless transformer, no fitting required."""
        return self

    def _apply_steps(self, value):
        """
        Applies pipeline to single value.

        Parameters
        ----------
        value : str
            The string value to apply transformations to.

        Returns
        -------
        str
            The transformed value.
        """
        for func, args, kwargs in self._pipeline:
            value = func(value, *args, **kwargs)
        return value

    def transform(self, X):
        """
        Transforms (columns of) a data frame of using the pipeline steps.
        Note: if no columns were specified in the constructor, selects only
        the columns with data type `object`.

        Parameters
        ----------
        X : pandas.DataFrame
            The pandas data frame to transform.

        Returns
        -------
        pandas.DataFrame
            The transformed pandas data frame.
        """

        # Column selection
        columns = self._columns or X.select_dtypes(include=["object"])

        # Build transformations
        funcs = {}
        for col in columns:
            funcs.update({col: X[col].map(self._apply_steps)})

        return X.assign(**funcs)
