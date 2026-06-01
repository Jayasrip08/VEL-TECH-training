# Your first Python script
name = 'Ravi'          # string
age = 21               # integer
gpa = 8.5              # float
is_student = True      # boolean

print('Name:', name)
print('Age:', age)
print('Type of age:', type(age))

# f-strings — modern way to format
print(f'Hello {name}! You are {age} years old')




# Taking input from user
user_name = input('Enter your name: ')
user_age = int(input('Enter your age: '))
print(f'In 5 years, {user_name} will be {user_age+5}')
