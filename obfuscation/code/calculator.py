import sys

from package import addition, differencce, multiply

sys.path.append('../')


def processValues(value1, value2):

    add = addition.getAddition(value1, value2)
    sub = differencce.getSubtraction(value1, value2)
    mult =multiply.getMultiplication(value1, value2)


    print("Addition Result :: " + str(add))
    print("Subtraction Result :: " + str(sub))
    print("Multiplication Result :: " + str(mult))



if __name__ == "__main__":
    value1 = 5
    value2 = 3
    processValues(value1, value2)
