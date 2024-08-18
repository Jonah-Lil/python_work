guests = ['Beau Miles','Scott Pendlebury','Tim Cahill']

for guest in guests:
    print(f"\nGood evening {guest}, would you like to join me for dinner?")

print(len(guests))

print(f"\n{guests[1]} cannot make it for dinner.")

del guests[1]
guests.append('Wayne Rooney')

for guest in guests:
    print(f"\nGood evening {guest}, would you like to join me for dinner?")

print("\nHello guests, there is space for three more to attend dinner.")

guests.insert(0,'Euan McGuire')
guests.insert(1,'Travis Scott')
guests.append('Lisa Nguyen')

for guest in guests:
    print(f"\nGood evening {guest}, would you like to join me for dinner?")

print("\nUnfortunately there is now only space for two guests.")

guests.pop(0)
print(f"\nSorry {guests[0]}, we will not be able to invite you for dinner.")

guests.pop(0)
print(f"\nSorry {guests[0]}, we will not be able to invite you for dinner.")

guests.pop(0)
print(f"\nSorry {guests[0]}, we will not be able to invite you for dinner.")

guests.pop(0)
print(f"\nSorry {guests[0]}, we will not be able to invite you for dinner.")

for guest in guests:
    print(f"\n{guest}, you are still invited to dinner.")

del guests[0]
del guests[0]

print(guests)