
def armstrong(number):
    
    num_str = str(number)
    num_digits = len(num_str)
    
    
    armstrong_sum = 0
    for i in num_str:
       armstrong_sum += int(i) ** num_digits

    return armstrong_sum == number


num = int(input("Enter a number: "))

if  armstrong(num):
    print('Armstrong number.')
else:
    print('not an Armstrong number.')
