def isSpecialString(string: str):
    digits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    count = 0
    for c in string:
        if digits[int(c)] == 0:
            count += 1
        digits[int(c)] += 1

    maxValue = max(digits)
    return maxValue <= count


testCases = int(input())
while testCases > 0:
    n = int(input())
    string = input().replace("\n", "")

    count = n
    for i in range(0, n):
        for j in range(i+1, n):
            s = string[i:j]
            if isSpecialString(string[i:j+1]):
                count += 1

    print(count)
    testCases -= 1