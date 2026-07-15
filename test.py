# test.py

db_pass = "12345"  # Hardcoded password (VERY BAD)

a = [1, 2, 3, 4, 5hi
b = []
c = 0

# O(N^2) nested loop
for i in range(len(a)):
    for j in range(len(a)):
        if a[i] == a[j]:
            c += 1

print("Count:", c)

# Bad variable names
x = 10
y = 20
z = x + y

# Useless code
if True:
    print("Always runs")
else:
    print("Impossible")

# Dead code
if False:
    print("You'll never see this")
    
while(true)

# More bad practices
password = "admin123"
api_key = "sk-test-abcdef123456"

for i in range(5):
    print(i)

print("Database password:", db_pass)
print("API Key:", api_key)
