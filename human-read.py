import os
import humanize

# 文件路径
file_path = "/Users/lxz/Library/CloudStorage/GoogleDrive-colorfool42@gmail.com (2023-6-2 08:04)/我的云端硬盘/大米和小米工作中表格/不常用的专业资料/言语治疗中心三折页.pdf"

# 获取文件大小
file_size = os.path.getsize(file_path)

# 使用 humanize.naturalsize 格式化文件大小
# binary=true指除以1024，false指除以1000
readable_size = humanize.naturalsize(file_size, binary=True)

print(readable_size)
