# Supported Docstring format

You can read about available docstring formats in this article: [Docstring Formats](https://realpython.com/documenting-python-code/#docstring-formats)

We opt for Google style which is described here: [PyGuide Functions and Methods](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#383-functions-and-methods)

You can use the following docstring as a reference:

```py title="test.py"
def test(name: str, age: int, is_student: bool, *args: str, **kwargs: int) -> None:
    """
    The test function...
    
    Args:
        name (str): name of the applicant
        age (int): age of the applicant
        is_student (bool): if the applicant is student or not
        *args (str): some variable length arguments
        **kwargs (int): keyword arguments
        
    Return: None
    """
```
