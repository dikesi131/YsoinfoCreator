import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Set, Dict
from .collect_input import CollectInput  # type: ignore


class SaveResult:
    """保存生成结果到SQLite数据库"""

    def __init__(self, db_path: str = "social_eng_results.db"):
        self.db_path = Path(db_path)
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self._init_database()

    def _init_database(self) -> None:
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # 创建生成任务表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS generation_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    personal_info TEXT,  -- JSON格式存储个人信息
                    created_at DATETIME NOT NULL,
                    username_count INTEGER DEFAULT 0,
                    password_count INTEGER DEFAULT 0,
                    total_count INTEGER DEFAULT 0
                )
            ''')

            # 创建用户名结果表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usernames (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    created_at DATETIME NOT NULL,
                    FOREIGN KEY (task_id) REFERENCES generation_tasks (id),
                    UNIQUE(task_id, username)
                )
            ''')

            # 创建密码结果表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    password TEXT NOT NULL,
                    created_at DATETIME NOT NULL,
                    FOREIGN KEY (task_id) REFERENCES generation_tasks (id),
                    UNIQUE(task_id, password)
                )
            ''')

            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_usernames_task_id ON usernames (task_id)')  # noqa
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_passwords_task_id ON passwords (task_id)')  # noqa
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON generation_tasks (created_at)')  # noqa

            conn.commit()

    def save_generation_result(self, name: str, description: str,
                               personal_info: CollectInput,
                               usernames: Set[str],
                               passwords: Set[str]) -> int:
        """保存一次生成的完整结果
        Args:
            name (str): 任务名称
            description (str): 任务描述
            personal_info (CollectInput): 个人信息对象
            usernames (Set[str]): 生成的用户名集合
            passwords (Set[str]): 生成的密码集合
        Returns:
            int: 任务ID, 如果保存失败则返回-1
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 保存任务信息
                task_id = self._save_task(cursor, name, description,
                                          personal_info,
                                          len(usernames), len(passwords))

                # 保存用户名
                if usernames:
                    self._save_usernames(cursor, task_id, usernames)

                # 保存密码
                if passwords:
                    self._save_passwords(cursor, task_id, passwords)

                conn.commit()
                print(f"✅ 生成结果已保存到数据库, 任务ID: {task_id}")
                return task_id

        except Exception as e:
            print(f"❌ 保存结果失败: {e}")
            return -1

    def _save_task(self, cursor: sqlite3.Cursor, name: str, description: str,
                   personal_info: CollectInput, username_count: int,
                   password_count: int) -> int:
        """保存任务信息
        Args:
            cursor (sqlite3.Cursor): 数据库游标
            name (str): 任务名称
            description (str): 任务描述
            personal_info (CollectInput): 个人信息对象
            username_count (int): 用户名数量
            password_count (int): 密码数量
        Returns:
            int: 任务ID
        """
        personal_info_json = json.dumps(personal_info.to_dict(),
                                        ensure_ascii=False)

        # 创建时间精确到年月日小时
        created_at = datetime.now().strftime(self.time_format)

        cursor.execute('''
            INSERT INTO generation_tasks
            (name, description, personal_info, created_at, username_count,
                       password_count, total_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            name,
            description,
            personal_info_json,
            created_at,
            username_count,
            password_count,
            username_count + password_count
        ))

        if cursor.lastrowid is None:
            raise RuntimeError("Failed to insert task, lastrowid is None")
        return cursor.lastrowid

    def _save_usernames(self, cursor: sqlite3.Cursor, task_id: int,
                        usernames: Set[str]) -> None:
        """批量保存用户名
        Args:
            cursor (sqlite3.Cursor): 数据库游标
            task_id (int): 任务ID
            usernames (Set[str]): 用户名集合
        """
        current_time = datetime.now().strftime(self.time_format)

        username_data = [
            (task_id, username, current_time)
            for username in usernames
        ]

        cursor.executemany('''
            INSERT OR IGNORE INTO usernames (task_id, username, created_at)
            VALUES (?, ?, ?)
        ''', username_data)

    def _save_passwords(self, cursor: sqlite3.Cursor, task_id: int,
                        passwords: Set[str]) -> None:
        """批量保存密码"""
        current_time = datetime.now().strftime(self.time_format)

        password_data = [
            (task_id, password, current_time)
            for password in passwords
        ]

        cursor.executemany('''
            INSERT OR IGNORE INTO passwords (task_id, password, created_at)
            VALUES (?, ?, ?)
        ''', password_data)

    def update_task_description(self, task_id: int, description: str) -> bool:
        """更新任务描述"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE generation_tasks
                    SET description = ?
                    WHERE id = ?
                ''', (description, task_id))

                if cursor.rowcount > 0:
                    conn.commit()
                    print(f"✅ 任务 {task_id} 描述已更新")
                    return True
                else:
                    print(f"⚠️ 任务 {task_id} 不存在")
                    return False

        except Exception as e:
            print(f"❌ 更新任务描述失败: {e}")
            return False

    def delete_task(self, task_id: int) -> bool:
        """删除任务及其所有相关数据"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 删除用户名
                cursor.execute('DELETE FROM usernames WHERE task_id = ?',
                               (task_id,))
                username_deleted = cursor.rowcount

                # 删除密码
                cursor.execute('DELETE FROM passwords WHERE task_id = ?',
                               (task_id,))
                password_deleted = cursor.rowcount

                # 删除任务
                cursor.execute('DELETE FROM generation_tasks WHERE id = ?',
                               (task_id,))
                task_deleted = cursor.rowcount

                if task_deleted > 0:
                    conn.commit()
                    print(f"✅ 任务 {task_id} 已删除 (用户名: {username_deleted}, 密码: {password_deleted})")  # noqa
                    return True
                else:
                    print(f"⚠️ 任务 {task_id} 不存在")
                    return False

        except Exception as e:
            print(f"❌ 删除任务失败: {e}")
            return False

    def get_database_stats(self) -> Dict[str, int]:
        """获取数据库统计信息"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 统计任务数量
                cursor.execute('SELECT COUNT(*) FROM generation_tasks')
                task_count = cursor.fetchone()[0]

                # 统计用户名总数
                cursor.execute('SELECT COUNT(*) FROM usernames')
                username_count = cursor.fetchone()[0]

                # 统计密码总数
                cursor.execute('SELECT COUNT(*) FROM passwords')
                password_count = cursor.fetchone()[0]

                # 统计唯一用户名数量
                cursor.execute('SELECT COUNT(DISTINCT username) FROM usernames')  # noqa
                unique_username_count = cursor.fetchone()[0]

                # 统计唯一密码数量
                cursor.execute('SELECT COUNT(DISTINCT password) FROM passwords')  # noqa
                unique_password_count = cursor.fetchone()[0]

                return {
                    'total_tasks': task_count,
                    'total_usernames': username_count,
                    'total_passwords': password_count,
                    'unique_usernames': unique_username_count,
                    'unique_passwords': unique_password_count,
                    'total_entries': username_count + password_count
                }

        except Exception as e:
            print(f"❌ 获取数据库统计失败: {e}")
            return {}

    def export_to_files(self, task_id: int,
                        output_dir: str = "export") -> bool:
        """将指定任务的结果导出到文件"""
        try:
            from .read_result import ReadResult  # type: ignore

            reader = ReadResult(str(self.db_path))

            # 获取任务信息
            task = reader.get_task_by_id(task_id)
            if not task:
                print(f"❌ 任务 {task_id} 不存在")
                return False

            # 创建输出目录
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)

            # 获取用户名和密码
            usernames = reader.get_usernames_by_task(task_id)
            passwords = reader.get_passwords_by_task(task_id)

            # 导出用户名
            username_file = output_path / f"usernames_task_{task_id}.txt"
            with open(username_file, 'w', encoding='utf-8') as f:
                for username in sorted(usernames):
                    f.write(username + '\n')

            # 导出密码
            password_file = output_path / f"passwords_task_{task_id}.txt"
            with open(password_file, 'w', encoding='utf-8') as f:
                for password in sorted(passwords):
                    f.write(password + '\n')

            # 导出任务信息
            info_file = output_path / f"task_{task_id}_info.json"
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(task, f, ensure_ascii=False, indent=2)

            print(f"✅ 任务 {task_id} 已导出到 {output_dir}")
            print(f"   📁 用户名文件: {username_file}")
            print(f"   📁 密码文件: {password_file}")
            print(f"   📁 任务信息: {info_file}")

            return True

        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False
