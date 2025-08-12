import re
from typing import Set
from pypinyin import lazy_pinyin


class NamePinyinCreator:
    """生成姓名拼音组合"""

    def __init__(self, name_zh: str, nickname_zh: str = "") -> None:
        self.name_zh = name_zh.strip()
        self.nickname_zh = nickname_zh.strip()

    def create_pinyin_combinations(self, name: str) -> Set[str]:
        """为单个中文名生成拼音组合"""
        if not name or not self._is_chinese(name):
            return set()

        combinations = set()

        # 获取拼音
        full_pinyin = lazy_pinyin(name)
        first_letters = [py[0].lower() for py in full_pinyin]

        # 1. 全拼连写 (如: zhangsan)
        combinations.add(''.join(full_pinyin))

        # 2. 全拼用点分隔 (如: zhang.san)
        combinations.add('.'.join(full_pinyin))

        # 3. 全拼用下划线分隔 (如: zhang_san)
        combinations.add('_'.join(full_pinyin))

        # 4. 全拼用横线分隔 (如: zhang-san)
        combinations.add('-'.join(full_pinyin))

        # 5. 首字母缩写 (如: zs)
        combinations.add(''.join(first_letters))

        # 6. 姓全拼+名首字母 (如: zhangs)
        # if len(full_pinyin) >= 2:
        #     combinations.add(full_pinyin[0] + ''.join(first_letters[1:]))

        # 7. 姓首字母+名全拼 (如: zsan)
        # if len(full_pinyin) >= 2:
        #     combinations.add(first_letters[0] + ''.join(full_pinyin[1:]))

        # 8. 每个字首字母大写的组合
        for combo in list(combinations):
            if combo.replace('.', '').replace('_', '').replace('-', '').isalpha():  # noqa
                # 首字母大写
                combinations.add(combo.capitalize())
                # 每个单词首字母大写
                if '.' in combo:
                    combinations.add('.'.join(word.capitalize() for word in combo.split('.')))  # noqa
                elif '_' in combo:
                    combinations.add('_'.join(word.capitalize() for word in combo.split('_')))  # noqa
                elif '-' in combo:
                    combinations.add('-'.join(word.capitalize() for word in combo.split('-')))  # noqa

        # 9. 反向组合 (名+姓)
        # if len(full_pinyin) >= 2:
        #     reversed_full = full_pinyin[1:] + [full_pinyin[0]]
        #     reversed_letters = first_letters[1:] + [first_letters[0]]

        #     combinations.add(''.join(reversed_full))
        #     combinations.add('.'.join(reversed_full))
        #     combinations.add('_'.join(reversed_full))
        #     combinations.add('-'.join(reversed_full))
        #     combinations.add(''.join(reversed_letters))

        # 过滤太短的组合
        return {combo for combo in combinations if len(combo) >= 2}

    def _is_chinese(self, text: str) -> bool:
        """检查文本是否包含中文字符"""
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        return bool(chinese_pattern.search(text))

    def run(self) -> Set[str]:
        """生成所有拼音组合"""
        all_combinations = set()

        # 处理姓名
        if self.name_zh:
            all_combinations.update(self.create_pinyin_combinations(self.name_zh))  # noqa

        # 处理昵称
        if self.nickname_zh:
            all_combinations.update(self.create_pinyin_combinations(self.nickname_zh))  # noqa

        return all_combinations

    def get_family_given_combinations(self, name: str) -> Set[str]:
        """获取姓氏和名字的单独拼音组合"""
        if not name or not self._is_chinese(name):
            return set()

        combinations = set()
        full_pinyin = lazy_pinyin(name)

        if len(full_pinyin) >= 2:
            # 姓氏 (通常是第一个字)
            family_name = full_pinyin[0]
            combinations.add(family_name)
            combinations.add(family_name.capitalize())

            # 名字 (剩余的字)
            given_name = ''.join(full_pinyin[1:])
            combinations.add(given_name)
            combinations.add(given_name.capitalize())

            # 名字分开
            for given_char in full_pinyin[1:]:
                combinations.add(given_char)
                combinations.add(given_char.capitalize())

        return combinations
