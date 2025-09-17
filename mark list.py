sub1=88
sub2=89
sub3=90
sub4=99
sub5=87 

Total_mark = sub1+sub2+sub3+sub4+sub5
print('Total mark =',Total_mark,'/5')

percentage = Total_mark/5
print ('percentage =',percentage,'%')


if percentage >= 90:
    print('Grade = A+')
elif percentage <= 89 and percentage >= 80:
    print('Grade = A')
elif percentage <= 79 and percentage >= 70:
    print('Grade = B')
elif percentage <= 69 and percentage >= 60:
    print('Grade = C')  
elif percentage <= 59 and percentage >= 50:
    print('Grade = D')
else:
    print('Grade = F')

    
