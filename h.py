import requests
session = requests.Session()

def get_and_save(url, filename):
    # 获取网页内容
    response = session.get(url)
    text = response.text

    # 将内容写入文件
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

    return text

# 使用函数并指定文件名
get_and_save('https://news.ycombinator.com/', 'hacker_news.html')
