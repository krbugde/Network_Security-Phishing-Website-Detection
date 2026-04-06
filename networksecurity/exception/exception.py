## this code of exception is common for any project we make
from networksecurity.logging import logger
import sys
'''import sys
This imports the sys module, which gives Python access to system-specific functions.
Here, it is used to get details about where an error happened (file name, line number).'''

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name[{0}] line number[{1}] error message[{2}]".format(
        file_name,exc_tb.tb_lineno,str(error))
    
    return error_message
    

'''What it does:

This function takes two things:
error → the actual error message that happened
error_detail → the sys module, which can give info about the error
exc_info() gets info about the current exception:
_ → type of exception (we ignore it)
_ → value of exception (we ignore it)
exc_tb → traceback object (where the error happened)
| Part          | Meaning                    |
| ------------- | -------------------------- |
| `exc_tb.tb_frame`    | returns frame where error occurred |
| `exc_tb.f_code`      | returns code object                |
| `exc_tb.co_filename` | returns name of the python file where error occured    |

file_name → gets the name of the file where the error occurred
exc_tb.tb_lineno → gets the line number of the error
error_message → combines file name, line number, and actual error into a nice readable message
return error_message → gives back the formatted message
✅ In simple words: This function tells you exactly where an error happened in your code in a readable way.'''

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message
    
if __name__=='__main__':
    try:
        logger.logging.info("Enter try block")
        a=1/0
        print("this will not be printed",a)
    except Exception as e:
        raise CustomException(e, sys)
    except Exception as e:
        raise CustomException(e, sys)
    
'''What it does:

This creates your own type of error called CustomException instead of using the normal Python errors.
__init__ function:
Calls the normal Exception constructor with super().__init__(error_message)
Then it customizes the error message by using the error_message_detail function

__str__ function:
When you print this exception, it will show the custom error message (file name + line number + actual error)

✅ In simple words: Whenever an error happens, instead of just saying “Some error occurred”, this class will tell you exactly which file and line caused the error.'''


'''Ah! Let me explain that part **very clearly and simply**, step by step.

---

### 1️⃣ What is `__init__`?

* `__init__` is called a **constructor** in Python.
* It **runs automatically** when you create a new object of a class.
* Think of it as the **setup code** for your object.

Example:

```python
class Person:
    def __init__(self, name):
        self.name = name

p = Person("Kumudini")
print(p.name)  # Output: Kumudini
```

* Here, `__init__` **sets up the `name`** for the object `p`.

---

### 2️⃣ What is `Exception`?

* In Python, **`Exception` is the base class for all errors**.
* When you do `raise Exception("something went wrong")`, Python creates an object of this class with the message `"something went wrong"`.

---

### 3️⃣ What is `super()`?

* `super()` lets a class **call a method from its parent class**.
* Here, your `CustomException` **inherits from `Exception`**, so its parent is `Exception`.
* `super().__init__(error_message)` **calls the parent `Exception`’s constructor** to store the error message properly.

---

### 4️⃣ Why do we need it?

If you didn’t call `super().__init__(error_message)`:

* Python’s normal exception features like `print(e)` or `str(e)` **would not work properly**.
* By calling `super().__init__`, we make sure our custom exception behaves **exactly like a normal exception**, but with extra details.

---

### 5️⃣ Simple analogy

* Imagine `Exception` is a **normal backpack** that holds error messages.
* `CustomException` is your **custom decorated backpack**.
* `super().__init__(error_message)` puts your error message **inside the normal backpack**, then you can add extra decorations (like file name and line number) on top.

---

### 6️⃣ Example to show difference

```python
class MyError(Exception):
    def __init__(self, msg):
        # Without super(), this won't behave like a normal Exception
        self.msg = msg

try:
    raise MyError("Oops")
except MyError as e:
    print(e)  # Output: <__main__.MyError object at 0x...>
```

Notice it doesn’t print the message automatically!

---

```python
class MyError(Exception):
    def __init__(self, msg):
        super().__init__(msg)  # Calls Exception constructor
        self.msg = msg

try:
    raise MyError("Oops")
except MyError as e:
    print(e)  # Output: Oops
```

✅ Now it prints the message because the parent `Exception` knows how to handle it.

'''
'''if __name__=="__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("Divide by zero error")
        raise CustomException(e,sys)
        '''
    