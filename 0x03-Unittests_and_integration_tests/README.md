# Access Nested Map - Unit Testing

This project is part of the **ALX Backend Python - Unit Testing** module.  
It focuses on testing a custom function called `access_nested_map` using Python's built-in `unittest` framework along with `parameterized`.

---

## 🧠 Purpose

The goal is to write **unit tests** for the function `access_nested_map` located in `utils.py`.  
This function retrieves values from nested dictionaries using a sequence of keys (like a path).

---

## 🧪 What We Test

We cover:

- **Correct return values** using valid nested keys
- **Error handling** when the path is invalid
- Using the **@parameterized.expand** decorator to test multiple inputs

---

## 🧾 Example

```python
from utils import access_nested_map

result = access_nested_map({'a': {'b': {'c': 3}}}, ('a', 'b', 'c'))
print(result)  # Output: 3
