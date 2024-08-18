locations = ['Great Wall of China','Uluru','Patagonia','Hanoi','Tokyo']

print("Here is the original list:")
print(locations)

print("\nHere is the sorted list:")
print(sorted(locations))

print("\nHere is the original list again:")
print(locations)

print("\nHere is the list in reverse order:")
locations.reverse()
print(locations)

print("\nHere is the original list again:")
locations.reverse()
print(locations)

print("\nHere is the list in alphabetical order:")
locations.sort()
print(locations)

print("\nHere is the list in reverse alphabetical order:")
locations.sort(reverse=True)
print(locations)