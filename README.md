# StringTransformer

A configurable tranformer class for performing string-related operations. The StringTransformer
class allows you to chain string operations and then apply them to a pandas data frame.

## Usage

Using the `StringTransformer` class is very simple. First initialize an instance and then start
adding transformations to it:

```python
# Initialize the StringTransformer.
tfm = StringTransformer()

# Add functions for stripping white-space and converting to lower case
tfm.add(str.strip)
tfm.add(str.lower)
```

Next we apply the transformer to a pandas DataFrame:

```python
# Transform a dataframe
df = pd.DataFrame({
    "x": [1, 2, 3],
    "label": [" One ", " Two ", " Three "]
})
tfm.transform(df)
```

Note: The transformer will only transform te `label` column, because this column is of the `object`
data type. Column `x` will remain untouched.

A shorter version of the above code looks like this:

```python
# Initialize and add steps
tfm = StringTransformer() + str.strip + str.lower
```

If you need to supply arguments, you can use a tuple:

```python
# Initialize and add steps
tfm = StringTransformer() + (str.strip, ["_"]) + str.lower
```

When a list is supplied, the `StringTransformer` assumes that the list contains positional arguments
to the transformer function. When a dict is supplied, the `StringTransformer` assumes these are
keyworded arguments to the transformer function.

If you want to see which transformations are currently configured, use the `list_steps` method:

```python
# Return steps in the transformation pipeline
tfm.list_steps()
```

## Common transformations

The following common string transformations are defined in the `common_transforms.py` file:

- normalize: Removes accents from special characters.
- strip_punctuation: Strips puntuation from a string.
- multi_replace: Uses a dict to replace multiple characters in a string.
- hash_string: Hashes a string given a specified algorithm.
- split_camel: Splits a CamelCases string into words.
- snake_case: Makes a snake_cased string.

You can import these for use with the StringTransformer class.
