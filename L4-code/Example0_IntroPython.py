'''
Indentation refers to the spaces at the beginning of a code line.
Where in other programming languages the indentation in code is for readability only, 
the indentation in Python is very important.

Python uses indentation to indicate a block of code.
'''

if 5>2:
    print("hello")
    # will produce error
    print("hello")

# casting
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0
print(type(x))


'''
a = 4
A = "Sally"
#A will not overwrite a
'''
cryptoCurrencies = ["Bitcoin", "Ethereum", "Tether"]

print(cryptoCurrencies)
print(cryptoCurrencies[1])

words = ["rizz", "cringe", "lit"]
for w in words:
  print(w)

# print without newline
print('Hello, World!', end=' ')
print('Python is fun!')

# function
def my_function():
  print("Hello from a function")

my_function()

def my_name(fname, lname):
  print(fname + " " + lname)

my_name("Emil", "Refsnes")
