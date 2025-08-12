import argparse
from .settings import USAGE_EXAMPLE  # type: ignore


def get_parser() -> argparse.ArgumentParser:
    """
    创建并返回命令行参数解析器
    """

    parser = argparse.ArgumentParser(
            description="社会工程学字典生成工具 - 仅用于授权的安全研究",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=USAGE_EXAMPLE
        )

    # 基本参数
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='启动交互式模式')
    parser.add_argument('--info', type=str,
                        help='个人信息JSON文件路径')
    parser.add_argument('--output', '-o', type=str, default='output',
                        help='输出目录 (默认: output)')
    parser.add_argument('--db-path', type=str, default='social_eng_results.db',
                        help='数据库文件路径 (默认: social_eng_results.db)')

    # 个人信息参数
    parser.add_argument('--name-zh', type=str, help='中文姓名')
    parser.add_argument('--name-en', type=str, help='英文姓名')
    parser.add_argument('--nickname-zh', type=str, help='中文昵称')
    parser.add_argument('--nickname-en', type=str, help='英文昵称')
    parser.add_argument('--birthday', type=str, help='生日 (YYYY-MM-DD)')
    parser.add_argument('--email', type=str, help='邮箱地址')
    parser.add_argument('--phone', type=str, help='手机号码')
    parser.add_argument('--username', type=str, help='已知用户名')
    parser.add_argument('--company-en', type=str, help='英文公司名')
    parser.add_argument('--company-zh', type=str, help='中文公司名')
    parser.add_argument('--department-en', type=str, help='英文部门名')
    parser.add_argument('--department-zh', type=str, help='中文部门名')
    parser.add_argument('--special-chars', type=str,
                        help='密码中使用的特殊字符 (例: !@#$%)')
    parser.add_argument('--custom-affix', type=str,
                        help='自定义后缀/前缀，用逗号分隔 (例: 666,888,love)')
    parser.add_argument('--custom-years', type=str,
                        help='自定义年份，用逗号分隔 (例: 1995,2020)')

    # 数据库相关参数
    parser.add_argument('--load-task', type=int,
                        help='从数据库加载指定ID的任务')
    parser.add_argument('--list-tasks', action='store_true',
                        help='列出保存的任务')
    parser.add_argument('--search-tasks', type=str,
                        help='搜索任务 (按名称)')
    parser.add_argument('--export-task', type=int,
                        help='导出指定任务的结果')
    parser.add_argument('--delete-task', type=int,
                        help='删除指定任务')
    parser.add_argument('--db-stats', action='store_true',
                        help='显示数据库统计信息')
    parser.add_argument('--save-task-name', type=str,
                        help='保存到数据库时的任务名称')
    parser.add_argument('--save-task-desc', type=str,
                        help='保存到数据库时的任务描述')

    # 外部字典合并
    parser.add_argument('--merge-username', type=str,
                        help='要合并的外部用户名字典文件')
    parser.add_argument('--merge-password', type=str,
                        help='要合并的外部密码字典文件')

    return parser
