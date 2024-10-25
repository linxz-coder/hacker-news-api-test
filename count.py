from collections import defaultdict

text = "hello world"
char_count = defaultdict(int)  # 默认值是0
print(char_count)

for char in text:
    char_count[char] += 1
    print(char_count)

print(char_count)
