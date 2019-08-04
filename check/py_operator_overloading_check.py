class A:
    def __init__(self, num):
        self.num = num

    def __add__(self, other):
        return self.num + other.num
    
    def __str__(self):
        return str(self.num)

    def __eq__(self, other):
        if(self.num == other.num):
            return True
        else:
            return False

    def __lt__(self, other):
        if(self.num < other.num):
            return True
        else:
            return False

    def __gt__(self, other):
        if(self.num > other.num):
            return True
        else:
            return False

num1 = A(1)
num2 = A(3)
num3 = A(1)

if(num1 < num2):
    print("num1 is less than num2: ({0}, {1})".format(num1, num2))
else:
    print("num1 is greater than num2: ({0}, {1})".format(num1, num2))

if(num2 > num1):
    print("num2 is greater than num1: ({0}, {1})".format(num2, num1))
else:
    print("num2 is less than num1: ({0}, {1})".format(num2, num1))

if(num1 == num3):
    print("num1 is equal to num3: ({0}, {1})".format(num1, num3))
else:
    print("num1 is not equal to num3: ({0}, {1})".format(num1, num3))


print(num1+num2)
print(num1)

