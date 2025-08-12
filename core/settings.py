import os

# 常用前缀
COMMON_PREFIX = [
    "admin",
    "user",
    "test",
    "guest",
    "root",
    "star",
    "Admin",
    "User",
    "Test",
    "Guest",
    "Root",
    "Star"
]

# 常用后缀
COMMON_SUFFIX = [
    "1",
    "2",
    "3",
    "01",
    "02",
    "03",
    "123",
    "456",
    '520',
    '521',
    '666',
    "789",
    "000",
    "001",
    "002",
    "003",
    "0001",
    "0002",
    "0003",
    "111",
    "222",
    "1234",
    '1314',
    "12345",
    "123456",
    "123654",
    "123123",
    "123321",
    "1234567",
    "12345678",
    "123456789",
    "abc",
    "qwe",
    "xyz",
    "qwer"
    "pass",
    "welcome",
    "iloveyou"
]

REGULAR_YEARS = [
    "2025",
    "2024",
    "2023",
    "2022",
    "2021",
    "2020",
    "2019",
    "2018",
    "2008",
    "2003"
]

REGULAR_KEYBOARD_PASSWD = [
    "qwerty",
    "qweasd",
    "qweasdzxc",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
    "159753",
    "159357",
    "753159",
    "753951",
    "456852",
    "456258",
    "654258",
    "654852",
    "111111",
    "555555",
    "777888",
    "123123",
    "123321",
    "123456",
    "666666",
    "888888",
    "7895123",
    "3215987",
    "135798462",
    "795134862",
    "88888888",
    "1234567"
    "12345678"
    "123456789",
    "1234567890",
]

# 常见的连接符
COMMON_SEPARATORS = ['', '.', '_', '-', '@', '#', '$']

# 有效的特殊字符范围（用于验证）
VALID_SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;':\",./<>?~`"

# top100 common passwords from core/txt/top_100_pass.txt
with open(os.path.join(os.path.dirname(__file__), 'txt/top_100_pass.txt'),
          'r', encoding='utf-8') as f:
    TOP_100_COMMON_PASSWORDS = [line.strip() for line in f if line.strip()]

# 使用示例
USAGE_EXAMPLE = """
    使用示例:
    # 交互式模式
    python main.py --interactive

    # 从数据库加载任务
    python main.py --load-task 5

    # 查看保存的任务
    python main.py --list-tasks

    # 搜索任务
    python main.py --search-tasks "张三"

    # 导出任务结果
    python main.py --export-task 5 --output ./export

    # 从JSON文件加载个人信息
    python main.py --info personal_info.json --output ./output

    # 命令行直接指定信息
    python main.py --name-zh "张三" --birthday "1990-01-01" --company-zh "ABC公司"

    ⚠️  重要提醒:
    - 本工具仅用于授权的安全测试和研究
    - 使用前请确保获得适当的授权
    - 请遵守相关法律法规和道德准则
    - 禁止用于恶意攻击或非法入侵
    """
