import sys
import os
from pathlib import Path
from datetime import datetime

from core.collect_input import CollectInput
from core.combo import Combo
from core.save_result import SaveResult
from core.read_result import ReadResult
from core.get_args import get_parser
from typing import Dict, Set, Optional, Any


class SocialEngDictionaryTool:
    """社会工程学字典生成工具"""

    def __init__(self, db_path: str = "social_eng_results.db") -> None:
        self.personal_info: Optional[CollectInput] = None
        self.combo_generator = Combo()
        self.results: Dict[str, Set[str]] = {'usernames': set(),
                                             'passwords': set()}
        self.usernames_count: int = len(self.results['usernames'])
        self.passwords_count: int = len(self.results['passwords'])

        # database
        self.db_path = db_path
        self.save_handler = SaveResult(db_path)
        self.read_handler = ReadResult(db_path)

    def load_personal_info_from_file(self, file_path: str) -> bool:
        """从文件加载个人信息"""
        try:
            self.personal_info = CollectInput.from_json_file(file_path)
            print(f"✅ 成功从文件加载个人信息: {file_path}")
            return True
        except Exception as e:
            print(f"❌ 加载个人信息文件失败: {e}")
            return False

    def set_personal_info(self, **kwargs) -> bool:
        """设置个人信息"""
        try:
            self.personal_info = CollectInput(**kwargs)

            # 验证输入
            validation = self.personal_info.validate_input()
            invalid_fields = [field for field, valid in validation.items() if not valid]  # noqa

            if invalid_fields:
                print(f"⚠️  警告: 以下字段格式不正确: {', '.join(invalid_fields)}")

            print("✅ 个人信息设置完成")
            print(f"📋 信息摘要: {self.personal_info.get_summary()}")
            return True
        except Exception as e:
            print(f"❌ 设置个人信息失败: {e}")
            return False

    def generate_dictionaries(self) -> bool:
        """生成字典"""
        if not self.personal_info:
            print("❌ 请先设置个人信息")
            return False

        try:
            print("🚀 开始生成社会工程学字典...")

            # 生成组合
            self.results = self.combo_generator.generate_all_combinations(self.personal_info)  # noqa
            all_count = self.usernames_count + self.passwords_count

            print("✅ 字典生成完成!")
            print(f"   📝 用户名: {self.usernames_count} 个")
            print(f"   🔐 密码: {self.passwords_count} 个")
            print(f"   📊 总计: {all_count} 个条目")

            return True
        except Exception as e:
            print(f"❌ 生成字典失败: {e}")
            return False

    def merge_external_dictionary(self, file_path: str,
                                  dict_type: str) -> bool:
        """合并外部字典"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                external_dict = set(line.strip() for line in f if line.strip())

            if dict_type == 'username':
                before_count = self.usernames_count
                self.results['usernames'].update(external_dict)
                after_count = self.usernames_count
                print(f"✅ 合并外部用户名字典: 新增 {after_count - before_count} 个条目")
            elif dict_type == 'password':
                before_count = self.passwords_count
                self.results['passwords'].update(external_dict)
                after_count = self.passwords_count
                print(f"✅ 合并外部密码字典: 新增 {after_count - before_count} 个条目")
            else:
                print(f"❌ 不支持的字典类型: {dict_type}")
                return False

            return True
        except Exception as e:
            print(f"❌ 合并外部字典失败: {e}")
            return False

    def save_dictionaries(self, output_dir: str = "output") -> bool:
        """保存字典文件"""
        try:
            # 创建输出目录
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)

            # 保存用户名字典
            username_file = output_path / "usernames.txt"
            with open(username_file, 'w', encoding='utf-8') as f:
                for username in sorted(self.results['usernames']):
                    f.write(username + '\n')
            print(f"✅ 用户名字典已保存: {username_file}")

            # 保存密码字典
            password_file = output_path / "passwords.txt"
            with open(password_file, 'w', encoding='utf-8') as f:
                for password in sorted(self.results['passwords']):
                    f.write(password + '\n')
            print(f"✅ 密码字典已保存: {password_file}")

            # 保存个人信息备份
            if self.personal_info:
                info_file = output_path / "personal_info_backup.json"
                self.personal_info.save_to_json(str(info_file))
                print(f"📋 个人信息备份已保存: {info_file}")

            # 生成报告
            self._generate_report(output_path)

            return True
        except Exception as e:
            print(f"❌ 保存字典失败: {e}")
            return False

    def save_to_database(self, task_name: str, description: str = "") -> int:
        """保存当前结果到数据库"""
        if not self.personal_info:
            print("❌ 没有个人信息可保存")
            return -1

        if not self.results['usernames'] and not self.results['passwords']:
            print("❌ 没有生成结果可保存")
            return -1

        return self.save_handler.save_generation_result(
            task_name, description, self.personal_info,
            self.results['usernames'], self.results['passwords']
        )

    def load_from_database(self, task_id: int) -> bool:
        """从数据库加载之前的结果"""
        try:
            # 获取任务信息
            task = self.read_handler.get_task_by_id(task_id)
            if not task:
                print(f"❌ 任务 {task_id} 不存在")
                return False

            # 恢复个人信息
            from core.collect_input import CollectInput
            self.personal_info = CollectInput.from_dict(task['personal_info'])

            # 加载结果
            usernames = self.read_handler.get_usernames_by_task(task_id)
            passwords = self.read_handler.get_passwords_by_task(task_id)

            self.results = {
                'usernames': usernames,
                'passwords': passwords
            }

            print(f"✅ 已加载任务 {task_id}: {task['name']}")
            print(f"   📝 用户名: {len(usernames)} 个")
            print(f"   🔐 密码: {len(passwords)} 个")
            print(f"   📅 创建时间: {task['created_at']}")

            return True

        except Exception as e:
            print(f"❌ 从数据库加载失败: {e}")
            return False

    def list_saved_tasks(self, limit: int = 10) -> None:
        """列出保存的任务"""
        tasks = self.read_handler.get_all_tasks(limit=limit)

        if not tasks:
            print("📝 暂无保存的任务")
            return

        print(f"\n📋 最近 {len(tasks)} 个任务:")
        print("-" * 80)
        print(f"{'ID':<5} {'名称':<20} {'用户名':<8} {'密码':<8} {'创建时间':<20}")
        print("-" * 80)

        for task in tasks:
            created_at = task['created_at'][:19] if task['created_at'] else "未知"  # noqa
            print(f"{task['id']:<5} {task['name'][:18]:<20} {task['username_count']:<8} "  # noqa
                  f"{task['password_count']:<8} {created_at:<20}")

    def search_saved_tasks(self, pattern: str) -> None:
        """搜索保存的任务"""
        tasks = self.read_handler.search_tasks_by_name(pattern)

        if not tasks:
            print(f"🔍 未找到匹配 '{pattern}' 的任务")
            return

        print(f"\n🔍 搜索结果 ('{pattern}'):")
        print("-" * 80)
        print(f"{'ID':<5} {'名称':<20} {'用户名':<8} {'密码':<8} {'创建时间':<20}")
        print("-" * 80)

        for task in tasks:
            created_at = task['created_at'][:19] if task['created_at'] else "未知"  # noqa
            print(f"{task['id']:<5} {task['name'][:18]:<20} {task['username_count']:<8} "  # noqa
                  f"{task['password_count']:<8} {created_at:<20}")

    def show_database_stats(self) -> None:
        """显示数据库统计信息"""
        stats = self.save_handler.get_database_stats()

        if not stats:
            print("❌ 无法获取数据库统计信息")
            return

        print("\n📊 数据库统计信息:")
        print("-" * 30)
        print(f"  总任务数: {stats.get('total_tasks', 0)}")
        print(f"  总用户名: {stats.get('total_usernames', 0)}")
        print(f"  总密码数: {stats.get('total_passwords', 0)}")
        print(f"  唯一用户名: {stats.get('unique_usernames', 0)}")
        print(f"  唯一密码: {stats.get('unique_passwords', 0)}")
        print(f"  总条目数: {stats.get('total_entries', 0)}")

    def _generate_report(self, output_path: Path) -> None:
        """生成详细报告"""
        report_file = output_path / "generation_report.txt"

        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("社会工程学字典生成报告\n")
                f.write("=" * 60 + "\n\n")

                # 个人信息概览
                f.write("📋 个人信息概览:\n")
                f.write("-" * 30 + "\n")
                if self.personal_info:
                    info_dict = self.personal_info.to_dict()
                    for key, value in info_dict.items():
                        if value:  # 只显示非空值
                            f.write(f"  {key}: {value}\n")
                else:
                    f.write("  无个人信息\n")
                f.write("\n")

                # 字典统计
                all_count = self.usernames_count + self.passwords_count
                f.write("📊 字典统计:\n")
                f.write("-" * 30 + "\n")
                f.write(f"  用户名数量: {self.usernames_count}\n")
                f.write(f"  密码数量: {self.passwords_count}\n")
                f.write(f"  总计条目: {all_count}\n\n")

                # 示例展示
                f.write("🔍 字典示例:\n")
                f.write("-" * 30 + "\n")

                # 用户名示例
                f.write("用户名示例 (前10个):\n")
                usernames_sample = list(sorted(self.results['usernames']))[:10]
                for username in usernames_sample:
                    f.write(f"  {username}\n")
                f.write("\n")

                # 密码示例
                f.write("密码示例 (前10个):\n")
                passwords_sample = list(sorted(self.results['passwords']))[:10]
                for password in passwords_sample:
                    f.write(f"  {password}\n")
                f.write("\n")

                # 安全提醒
                f.write("⚠️  安全提醒:\n")
                f.write("-" * 30 + "\n")
                f.write("  1. 此工具仅用于授权的安全测试和研究\n")
                f.write("  2. 请遵守相关法律法规和道德准则\n")
                f.write("  3. 禁止用于恶意攻击或非法入侵\n")
                f.write("  4. 使用前请确保获得适当的授权\n")
                f.write("  5. 建议在隔离的测试环境中使用\n\n")

                # 免责声明
                f.write("📄 免责声明:\n")
                f.write("-" * 30 + "\n")
                f.write("  本工具仅供安全研究和教育目的使用。\n")
                f.write("  使用者需自行承担使用本工具的所有责任和风险。\n")
                f.write("  开发者不对任何滥用行为承担责任。\n")

            print(f"📋 详细报告已保存: {report_file}")
        except Exception as e:
            print(f"❌ 生成报告失败: {e}")

    def _run_load_mode(self) -> None:
        """运行加载模式"""
        self.list_saved_tasks(10)

        try:
            task_id = int(input("\n请输入要加载的任务ID: ").strip())
            if self.load_from_database(task_id):
                self._show_preview()

                # 询问是否导出
                export = input("\n📁 是否导出当前结果到文件? (y/N): ").strip().lower()
                if export == 'y':
                    output_dir = input("  输出目录 (默认: output): ").strip()
                    if not output_dir:
                        output_dir = "output"

                    self.save_dictionaries(output_dir)
        except ValueError:
            print("❌ 请输入有效的任务ID")

    def _run_search_mode(self) -> None:
        """运行搜索模式"""
        pattern = input("请输入搜索关键词: ").strip()
        if pattern:
            self.search_saved_tasks(pattern)

    def _run_export_mode(self) -> None:
        """运行导出模式"""
        self.list_saved_tasks(10)

        try:
            task_id = int(input("\n请输入要导出的任务ID: ").strip())
            output_dir = input("输出目录 (默认: export): ").strip()
            if not output_dir:
                output_dir = "export"

            self.save_handler.export_to_files(task_id, output_dir)
        except ValueError:
            print("❌ 请输入有效的任务ID")

    def _run_delete_mode(self) -> None:
        """运行删除模式"""
        self.list_saved_tasks(10)

        try:
            task_id = int(input("\n请输入要删除的任务ID: ").strip())

            # 确认删除
            confirm = input(f"⚠️ 确定要删除任务 {task_id} 吗? 此操作不可恢复! (y/N): ").strip().lower()  # noqa
            if confirm == 'y':
                if self.save_handler.delete_task(task_id):
                    print("✅ 任务删除成功")
                else:
                    print("❌ 任务删除失败")
            else:
                print("❌ 取消删除")
        except ValueError:
            print("❌ 请输入有效的任务ID")

    def _run_generate_mode(self) -> None:
        """运行生成模式"""
        print("🎯 社会工程学字典生成工具")
        print("=" * 50)
        print("⚠️  警告: 仅用于授权的安全测试!")
        print("=" * 50)

        # 收集个人信息
        print("\n📝 请输入目标个人信息 (留空跳过):")

        # 定义信息字段
        info_fields = [
            ("中文姓名", "name_zh", "例: 张三"),
            ("英文姓名", "name_en", "例: John Smith"),
            ("中文昵称", "nickname_zh", "例: 小张"),
            ("英文昵称", "nickname_en", "例: Johnny"),
            ("生日", "birthday", "例: 1990-01-01"),
            ("邮箱", "email", "例: user@example.com"),
            ("手机号", "phone", "例: 13800138000"),
            ("用户名", "username", "例: john123"),
            ("英文公司名", "company_en", "例: ABC Company"),
            ("中文公司名", "company_zh", "例: ABC公司"),
            ("英文部门", "department_en", "例: IT Department"),
            ("中文部门", "department_zh", "例: 信息技术部"),
        ]

        info_data: Dict[str, Any] = {}
        for display_name, field_name, example in info_fields:
            value = input(f"  {display_name} ({example}): ").strip()
            if value:
                info_data[field_name] = value

        # 特殊字符输入
        print("\n🔧 特殊字符设置:")
        print("  常用特殊字符参考: !@#$%^&*()_+-=[]{}|;':\",./<>?~`")
        special_chars = input("  请输入要使用的特殊字符 (例: !@#$%): ").strip()
        if special_chars:
            info_data['special_chars'] = special_chars
            print(f"  ✅ 已设置特殊字符: {special_chars}")
        else:
            print("  ⚠️ 将使用默认特殊字符")

        # 自定义后缀/前缀
        print("\n📎 自定义后缀/前缀 (可选):")
        custom_affix = input("  输入自定义后缀/前缀，用逗号分隔 (例: 666,888,love): ").strip()
        if custom_affix:
            affix_list = [item.strip() for item in custom_affix.split(',') if item.strip()]  # noqa
            if affix_list:
                info_data['common_affix'] = affix_list
                print(f"  ✅ 已添加自定义后缀/前缀: {', '.join(affix_list)}")

        # 自定义年份
        print("\n📅 自定义年份 (可选):")
        custom_years = input("  输入自定义年份，用逗号分隔 (例: 1995,2020,88): ").strip()
        if custom_years:
            years_list = [item.strip() for item in custom_years.split(',') if item.strip()]  # noqa
            if years_list:
                info_data['regular_years'] = years_list
                print(f"  ✅ 已添加自定义年份: {', '.join(years_list)}")

        # 设置个人信息
        if info_data:
            if not self.set_personal_info(**info_data):
                return
        else:
            print("⚠️ 未输入个人信息，将无法生成个性化字典")
            return

        # 验证特殊字符
        if self.personal_info and self.personal_info.special_chars:
            if not self.personal_info._validate_special_chars():
                print("⚠️ 警告: 输入的特殊字符包含无效字符，可能影响生成效果")

        # 询问是否合并外部字典
        print("\n🔗 外部字典合并 (可选):")
        merge_username = input("  用户名字典文件路径 (留空跳过): ").strip()
        merge_password = input("  密码字典文件路径 (留空跳过): ").strip()

        # 生成字典
        if not self.generate_dictionaries():
            return

        # 合并外部字典
        if merge_username and os.path.exists(merge_username):
            self.merge_external_dictionary(merge_username, 'username')
        elif merge_username:
            print(f"⚠️ 用户名字典文件不存在: {merge_username}")

        if merge_password and os.path.exists(merge_password):
            self.merge_external_dictionary(merge_password, 'password')
        elif merge_password:
            print(f"⚠️ 密码字典文件不存在: {merge_password}")

        # 询问是否保存到数据库
        save_to_db = input("\n💾 是否保存结果到数据库? (Y/n): ").strip().lower()
        if save_to_db != 'n':
            task_name = input("  任务名称: ").strip()
            if not task_name:
                task_name = f"任务_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            description = input("  任务描述 (可选): ").strip()

            task_id = self.save_to_database(task_name, description)
            if task_id > 0:
                print(f"✅ 结果已保存到数据库, 任务ID: {task_id}")

        # 询问是否导出到文件
        export_to_file = input("\n📁 是否导出到文件? (Y/n): ").strip().lower()
        if export_to_file != 'n':
            output_dir = input("  输出目录 (默认: output): ").strip()
            if not output_dir:
                output_dir = "output"

            self.save_dictionaries(output_dir)

        # 显示预览
        self._show_preview()

    def run_interactive_mode(self) -> None:
        """交互式运行模式"""
        print("🎯 社会工程学字典生成工具")
        print("=" * 50)
        print("⚠️  警告: 仅用于授权的安全测试!")
        print("=" * 50)

        while True:
            print("\n🎯 主菜单:")
            print("  1. 生成新字典")
            print("  2. 从数据库加载历史任务")
            print("  3. 查看保存的任务列表")
            print("  4. 搜索任务")
            print("  5. 查看数据库统计")
            print("  6. 导出任务结果")
            print("  7. 删除任务")
            print("  0. 退出")

            choice = input("\n请选择操作 (0-7): ").strip()

            if choice == '1':
                self._run_generate_mode()
            elif choice == '2':
                self._run_load_mode()
            elif choice == '3':
                self.list_saved_tasks(20)
            elif choice == '4':
                self._run_search_mode()
            elif choice == '5':
                self.show_database_stats()
            elif choice == '6':
                self._run_export_mode()
            elif choice == '7':
                self._run_delete_mode()
            elif choice == '0':
                print("👋 再见!")
                break
            else:
                print("❌ 无效选择，请重试")

    def _show_preview(self) -> None:
        """显示字典预览"""
        print("\n👀 字典预览:")
        print("-" * 30)

        # 用户名预览
        usernames_sample = list(sorted(self.results['usernames']))[:5]
        print("用户名示例:")
        for username in usernames_sample:
            print(f"  {username}")

        if len(self.results['usernames']) > 5:
            print(f"  ... 还有 {len(self.results['usernames']) - 5} 个")

        print()

        # 密码预览
        passwords_sample = list(sorted(self.results['passwords']))[:5]
        print("密码示例:")
        for password in passwords_sample:
            print(f"  {password}")

        if len(self.results['passwords']) > 5:
            print(f"  ... 还有 {len(self.results['passwords']) - 5} 个")


def main():
    """主函数"""
    parser = get_parser()

    # 解析参数
    args = parser.parse_args()

    # 创建工具实例
    tool = SocialEngDictionaryTool(args.db_path)

    # 数据库操作
    if args.list_tasks:
        tool.list_saved_tasks(20)
        return

    if args.search_tasks:
        tool.search_saved_tasks(args.search_tasks)
        return

    if args.db_stats:
        tool.show_database_stats()
        return

    if args.load_task:
        if tool.load_from_database(args.load_task):
            if tool.save_dictionaries(args.output):
                print(f"\n🎉 任务结果已导出到 {args.output} 目录")
                tool._show_preview()
        return

    if args.export_task:
        tool.save_handler.export_to_files(args.export_task, args.output)
        return

    if args.delete_task:
        confirm = input(f"⚠️ 确定要删除任务 {args.delete_task} 吗? 此操作不可恢复! (y/N): ").strip().lower()  # noqa
        if confirm == 'y':
            tool.save_handler.delete_task(args.delete_task)
        else:
            print("❌ 取消删除")
        return

    # 交互式模式
    if args.interactive:
        tool.run_interactive_mode()
        return

    # 从文件加载个人信息
    if args.info:
        if not os.path.exists(args.info):
            print(f"❌ 个人信息文件不存在: {args.info}")
            return
        if not tool.load_personal_info_from_file(args.info):
            return
    else:
        # 从命令行参数构建个人信息
        info_dict = {}

        # 映射命令行参数到字段名
        field_mapping = {
            'name_zh': args.name_zh,
            'name_en': args.name_en,
            'nickname_zh': args.nickname_zh,
            'nickname_en': args.nickname_en,
            'birthday': args.birthday,
            'email': args.email,
            'phone': args.phone,
            'username': args.username,
            'company_en': args.company_en,
            'company_zh': args.company_zh,
            'department_en': args.department_en,
            'department_zh': args.department_zh,
        }

        # 收集非空参数
        for field, value in field_mapping.items():
            if value:
                info_dict[field] = value

        if not info_dict:
            print("❌ 请提供个人信息或使用 --interactive 模式")
            print("使用 --help 查看详细用法")
            return

        if not tool.set_personal_info(**info_dict):
            return

    if args.special_chars:
        info_dict['special_chars'] = args.special_chars
    if args.custom_affix:
        affix_list = [item.strip() for item in args.custom_affix.split(',') if item.strip()]  # noqa
        if affix_list:
            info_dict['common_affix'] = affix_list
    if args.custom_years:
        years_list = [item.strip() for item in args.custom_years.split(',') if item.strip()]  # noqa
        if years_list:
            info_dict['regular_years'] = years_list

    # 生成字典
    if not tool.generate_dictionaries():
        return

    # 合并外部字典
    if args.merge_username:
        if os.path.exists(args.merge_username):
            tool.merge_external_dictionary(args.merge_username, 'username')
        else:
            print(f"⚠️ 用户名字典文件不存在: {args.merge_username}")

    if args.merge_password:
        if os.path.exists(args.merge_password):
            tool.merge_external_dictionary(args.merge_password, 'password')
        else:
            print(f"⚠️ 密码字典文件不存在: {args.merge_password}")

    # 保存字典
    if tool.save_dictionaries(args.output):
        print(f"\n🎉 字典生成完成! 请查看 {args.output} 目录")
        tool._show_preview()

    # 生成字典后，如果指定了任务名称，则保存到数据库
    if args.save_task_name and tool.personal_info:
        task_id = tool.save_to_database(
            args.save_task_name,
            args.save_task_desc or ""
        )
        if task_id > 0:
            print(f"✅ 结果已保存到数据库, 任务ID: {task_id}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断程序")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
