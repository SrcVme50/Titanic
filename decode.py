import sqlite3
import base64

# 连接 SQLite 数据库
db_path = "gitea.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询 user 表中的 passwd, salt, name
cursor.execute("SELECT passwd, salt, name FROM user")
rows = cursor.fetchall()

# 处理数据并写入 gitea.hashes
output_file = "gitea.hashes"

with open(output_file, "w") as f:
    for passwd_hex, salt_hex, name in rows:
        # 将 Hex 解码为原始字节数据
        passwd_bytes = bytes.fromhex(passwd_hex)
        salt_bytes = bytes.fromhex(salt_hex)

        # 转换为 Base64
        passwd_b64 = base64.b64encode(passwd_bytes).decode()
        salt_b64 = base64.b64encode(salt_bytes).decode()

        # 格式化输出
        hash_entry = f"sha256:50000:{salt_b64}:{passwd_b64}\n"
        f.write(hash_entry)
        print(hash_entry.strip())  # 也在终端打印

# 关闭数据库连接
conn.close()
