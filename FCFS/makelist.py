finish = ""
nums = []
while finish is not "done":
    content = int(input("Enter a number: "))
    if content == 999:
        break
    nums.append(content)

print(nums)
