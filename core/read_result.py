import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple


class ReadResult:
    """从SQLite数据库读取保存的结果"""

    def __init__(self, db_path: str = "social_eng_results.db"):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            print(f"⚠️ 数据库文件不存在: {db_path}")

    def get_all_tasks(self, limit: int = 100,
                      offset: int = 0) -> List[Dict[str, Any]]:
        """获取所有任务列表
        Args:
            limit (int): 每页数量, 默认100
            offset (int): 偏移量, 默认0
        Returns:
            List[Dict[str, Any]]: 任务列表, 每个任务包含ID、名称、描述、创建时间等信息
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT id, name, description, created_at,
                           username_count, password_count, total_count
                    FROM generation_tasks
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                ''', (limit, offset))

                tasks = []
                for row in cursor.fetchall():
                    tasks.append({
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'created_at': row['created_at'],
                        'username_count': row['username_count'],
                        'password_count': row['password_count'],
                        'total_count': row['total_count']
                    })

                return tasks

        except Exception as e:
            print(f"❌ 获取任务列表失败: {e}")
            return []

    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取任务详细信息
        Args:
            task_id (int): 任务ID
        Returns:
            Optional[Dict[str, Any]]: 任务详细信息, 包含ID、名称、描述、个人信息、创建时间等
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT * FROM generation_tasks WHERE id = ?
                ''', (task_id,))

                row = cursor.fetchone()
                if row:
                    personal_info = json.loads(row['personal_info']) if row['personal_info'] else {}  # noqa

                    return {
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'personal_info': personal_info,
                        'created_at': row['created_at'],
                        'username_count': row['username_count'],
                        'password_count': row['password_count'],
                        'total_count': row['total_count']
                    }

                return None

        except Exception as e:
            print(f"❌ 获取任务详情失败: {e}")
            return None

    def get_usernames_by_task(self, task_id: int,
                              limit: Optional[int] = None) -> Set[str]:
        """获取指定任务的用户名
        Args:
            task_id (int): 任务ID
            limit (Optional[int]): 限制返回的用户名数量, 默认不限制
        Returns:
            Set[str]: 用户名集合
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                query = 'SELECT username FROM usernames WHERE task_id = ? ORDER BY username'  # noqa
                params = [task_id]

                if limit:
                    query += ' LIMIT ?'
                    params.append(limit)

                cursor.execute(query, params)

                return {row[0] for row in cursor.fetchall()}

        except Exception as e:
            print(f"❌ 获取用户名失败: {e}")
            return set()

    def get_passwords_by_task(self, task_id: int,
                              limit: Optional[int] = None) -> Set[str]:
        """获取指定任务的密码
        Args:
            task_id (int): 任务ID
            limit (Optional[int]): 限制返回的密码数量, 默认不限制
        Returns:
            Set[str]: 密码集合
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                query = 'SELECT password FROM passwords WHERE task_id = ? ORDER BY password'  # noqa
                params = [task_id]

                if limit:
                    query += ' LIMIT ?'
                    params.append(limit)

                cursor.execute(query, params)

                return {row[0] for row in cursor.fetchall()}

        except Exception as e:
            print(f"❌ 获取密码失败: {e}")
            return set()

    def search_tasks_by_name(self, name_pattern: str) -> List[Dict[str, Any]]:
        """根据名称模糊搜索任务
        Args:
            name_pattern (str): 任务名称模式
        Returns:
            List[Dict[str, Any]]: 匹配的任务列表, 每个任务包含ID、名称、描述、创建时间等信息
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT id, name, description, created_at,
                           username_count, password_count, total_count
                    FROM generation_tasks
                    WHERE name LIKE ?
                    ORDER BY created_at DESC
                ''', (f'%{name_pattern}%',))

                tasks = []
                for row in cursor.fetchall():
                    tasks.append({
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'created_at': row['created_at'],
                        'username_count': row['username_count'],
                        'password_count': row['password_count'],
                        'total_count': row['total_count']
                    })

                return tasks

        except Exception as e:
            print(f"❌ 搜索任务失败: {e}")
            return []

    def search_usernames(self, pattern: str,
                         task_id: Optional[int] = None) -> List[Tuple[str, int]]:  # noqa
        """搜索用户名
        Args:
            pattern (str): 用户名模式
            task_id (Optional[int]): 任务ID, 如果提供则只搜索该任务下的用户名
        Returns:
            List[Tuple[str, int]]: 匹配的用户名和任务ID列表
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                if task_id:
                    cursor.execute('''
                        SELECT username, task_id FROM usernames
                        WHERE username LIKE ? AND task_id = ?
                        ORDER BY username
                    ''', (f'%{pattern}%', task_id))
                else:
                    cursor.execute('''
                        SELECT username, task_id FROM usernames
                        WHERE username LIKE ?
                        ORDER BY username
                    ''', (f'%{pattern}%',))

                return cursor.fetchall()

        except Exception as e:
            print(f"❌ 搜索用户名失败: {e}")
            return []

    def search_passwords(self, pattern: str,
                         task_id: Optional[int] = None) -> List[Tuple[str, int]]:  # noqa
        """搜索密码
        Args:
            pattern (str): 密码模式
            task_id (Optional[int]): 任务ID, 如果提供则只搜索该任务下的密码
        Returns:
            List[Tuple[str, int]]: 匹配的密码和任务ID列表
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                if task_id:
                    cursor.execute('''
                        SELECT password, task_id FROM passwords
                        WHERE password LIKE ? AND task_id = ?
                        ORDER BY password
                    ''', (f'%{pattern}%', task_id))
                else:
                    cursor.execute('''
                        SELECT password, task_id FROM passwords
                        WHERE password LIKE ?
                        ORDER BY password
                    ''', (f'%{pattern}%',))

                return cursor.fetchall()

        except Exception as e:
            print(f"❌ 搜索密码失败: {e}")
            return []

    def get_tasks_by_date_range(self, start_date: str,
                                end_date: str) -> List[Dict[str, Any]]:
        """根据日期范围获取任务
        Args:
            start_date (str): 起始日期, 格式为 'YYYY-MM-DD'
            end_date (str): 结束日期, 格式为 'YYYY-MM-DD'
        Returns:
            List[Dict[str, Any]]: 在指定日期范围内的任务列表, 每个任务包含ID、名称、描述、创建时间等信息
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT id, name, description, created_at,
                           username_count, password_count, total_count
                    FROM generation_tasks
                    WHERE created_at BETWEEN ? AND ?
                    ORDER BY created_at DESC
                ''', (start_date, end_date))

                tasks = []
                for row in cursor.fetchall():
                    tasks.append({
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'created_at': row['created_at'],
                        'username_count': row['username_count'],
                        'password_count': row['password_count'],
                        'total_count': row['total_count']
                    })

                return tasks

        except Exception as e:
            print(f"❌ 获取日期范围任务失败: {e}")
            return []

    def get_combined_results(self, task_ids: List[int]) -> Dict[str, Set[str]]:
        """合并多个任务的结果
        Args:
            task_ids (List[int]): 任务ID列表
        Returns:
            Dict[str, Set[str]]: 合并后的用户名和密码集合
        """
        try:
            combined_usernames = set()
            combined_passwords = set()

            for task_id in task_ids:
                usernames = self.get_usernames_by_task(task_id)
                passwords = self.get_passwords_by_task(task_id)

                combined_usernames.update(usernames)
                combined_passwords.update(passwords)

            return {
                'usernames': combined_usernames,
                'passwords': combined_passwords
            }

        except Exception as e:
            print(f"❌ 合并结果失败: {e}")
            return {'usernames': set(), 'passwords': set()}

    def get_statistics_by_task(self, task_id: int) -> Dict[str, Any]:
        """获取指定任务的统计信息
        Args:
            task_id (int): 任务ID
        Returns:
            Dict[str, Any]: 任务统计信息, 包含实际用户名数量、密码数量、用户名长度分布等
        """
        try:
            task = self.get_task_by_id(task_id)
            if not task:
                return {}

            # 获取实际数量（可能与存储的数量不同）
            usernames = self.get_usernames_by_task(task_id)
            passwords = self.get_passwords_by_task(task_id)

            # 分析用户名长度分布
            username_lengths = [len(u) for u in usernames]
            password_lengths = [len(p) for p in passwords]

            stats = {
                'task_info': task,
                'actual_username_count': len(usernames),
                'actual_password_count': len(passwords),
                'username_length_stats': {
                    'min': min(username_lengths) if username_lengths else 0,
                    'max': max(username_lengths) if username_lengths else 0,
                    'avg': sum(username_lengths) / len(username_lengths) if username_lengths else 0  # noqa
                },
                'password_length_stats': {
                    'min': min(password_lengths) if password_lengths else 0,
                    'max': max(password_lengths) if password_lengths else 0,
                    'avg': sum(password_lengths) / len(password_lengths) if password_lengths else 0  # noqa
                }
            }

            return stats

        except Exception as e:
            print(f"❌ 获取任务统计失败: {e}")
            return {}

    def export_all_unique_entries(self,
                                  output_dir: str = "export_all") -> bool:
        """导出所有唯一的用户名和密码"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 获取所有唯一用户名
                cursor.execute('SELECT DISTINCT username FROM usernames ORDER BY username')  # noqa
                unique_usernames = {row[0] for row in cursor.fetchall()}

                # 获取所有唯一密码
                cursor.execute('SELECT DISTINCT password FROM passwords ORDER BY password')  # noqa
                unique_passwords = {row[0] for row in cursor.fetchall()}

                # 创建输出目录
                output_path = Path(output_dir)
                output_path.mkdir(exist_ok=True)

                # 导出用户名
                username_file = output_path / "all_unique_usernames.txt"
                with open(username_file, 'w', encoding='utf-8') as f:
                    for username in sorted(unique_usernames):
                        f.write(username + '\n')

                # 导出密码
                password_file = output_path / "all_unique_passwords.txt"
                with open(password_file, 'w', encoding='utf-8') as f:
                    for password in sorted(unique_passwords):
                        f.write(password + '\n')

                print(f"✅ 所有唯一条目已导出到 {output_dir}")
                print(f"   📁 用户名: {len(unique_usernames)} 个")
                print(f"   📁 密码: {len(unique_passwords)} 个")

                return True

        except Exception as e:
            print(f"❌ 导出所有唯一条目失败: {e}")
            return False
