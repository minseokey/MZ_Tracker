

f = open("data/return2.txt", "r", encoding='utf-8')
token = []
text = f.readlines()
def text_clearing(text):
    import re
    hangul = re.compile('[^ㄱ-ㅣ가-힣]+')
    result = hangul.sub('', text)
    return result
for i in text:
    temp = []
    for j in i.strip().split():
        word = text_clearing(j)
        if word:
            temp.append(word)
    token.append(temp)

a = 0
for i in token:
    a += len(i)
print(a)
f.close()
