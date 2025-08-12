import re
from typing import Set
from itertools import combinations as iter_combinations, permutations as iter_permutations  # noqa


class NameInitialCreator:
    """生成姓名首字母组合"""

    def __init__(self, name_zh: str = "", name_en: str = "",
                 nickname_zh: str = "", nickname_en: str = "") -> None:
        self.name_zh = name_zh.strip()
        self.name_en = name_en.strip()
        self.nickname_zh = nickname_zh.strip()
        self.nickname_en = nickname_en.strip()

    def create_english_initials(self, name: str) -> Set[str]:
        """从英文名生成首字母组合"""
        if not name:
            return set()

        # 清理名字，只保留字母和空格
        clean_name = re.sub(r'[^a-zA-Z\s]', '', name)
        words = clean_name.split()

        if not words:
            return set()

        initial_combinations = set()

        # 1. 所有单词首字母 (如: John Smith -> js)
        initials = ''.join(word[0].lower() for word in words if word)
        if initials:
            initial_combinations.add(initials)
            initial_combinations.add(initials.upper())
            initial_combinations.add(initials.capitalize())

        # 2. 带点分隔的首字母 (如: j.s)
        if len(words) > 1:
            dotted = '.'.join(word[0].lower() for word in words if word)
            initial_combinations.add(dotted)
            initial_combinations.add(dotted.upper())

        # 3. 每个单词的首字母单独
        for word in words:
            if word:
                initial_combinations.add(word[0].lower())
                initial_combinations.add(word[0].upper())

        # 4. 名字首字母 + 姓氏 (如: j + smith -> jsmith)
        if len(words) >= 2:
            first_initial = words[0][0].lower()
            last_name = words[-1].lower()
            initial_combinations.add(first_initial + last_name)
            initial_combinations.add((first_initial + last_name).capitalize())

        # 5. 姓氏首字母 + 名字 (如: s + john -> sjohn)
        if len(words) >= 2:
            last_initial = words[-1][0].lower()
            first_name = words[0].lower()
            initial_combinations.add(last_initial + first_name)
            initial_combinations.add((last_initial + first_name).capitalize())

        return initial_combinations

    def create_chinese_initials(self, name: str) -> Set[str]:
        """从中文名生成首字母组合 (基于拼音)"""
        if not name:
            return set()

        try:
            from pypinyin import lazy_pinyin

            # 获取拼音首字母
            pinyin_list = lazy_pinyin(name)
            initials = ''.join(py[0].lower() for py in pinyin_list)

            initial_combinations = set()
            initial_combinations.add(initials)
            initial_combinations.add(initials.upper())
            initial_combinations.add(initials.capitalize())

            # 如果是两个字以上，生成更多组合
            if len(pinyin_list) >= 2:
                # 姓氏首字母 + 名字首字母们
                family_initial = pinyin_list[0][0].lower()
                given_initials = ''.join(py[0].lower() for py in pinyin_list[1:])  # noqa

                initial_combinations.add(family_initial + given_initials)
                initial_combinations.add((family_initial + given_initials).upper())  # noqa

                # 每个字的首字母
                for py in pinyin_list:
                    initial_combinations.add(py[0].lower())
                    initial_combinations.add(py[0].upper())

            return initial_combinations

        except ImportError:
            # 如果没有pypinyin，返回空集合
            return set()

    def create_mixed_initials(self) -> Set[str]:
        """创建中英文混合的首字母组合"""
        mixed_combinations = set()

        # 获取所有可能的首字母
        all_initials = []

        # 英文名首字母
        if self.name_en:
            en_words = re.sub(r'[^a-zA-Z\s]', '', self.name_en).split()
            for word in en_words:
                if word:
                    all_initials.append(word[0].lower())

        # 英文昵称首字母
        if self.nickname_en:
            en_nick_words = re.sub(r'[^a-zA-Z\s]', '',
                                   self.nickname_en).split()
            for word in en_nick_words:
                if word:
                    all_initials.append(word[0].lower())

        # 中文名首字母 (拼音)
        try:
            from pypinyin import lazy_pinyin

            if self.name_zh:
                zh_pinyin = lazy_pinyin(self.name_zh)
                for py in zh_pinyin:
                    all_initials.append(py[0].lower())

            if self.nickname_zh:
                zh_nick_pinyin = lazy_pinyin(self.nickname_zh)
                for py in zh_nick_pinyin:
                    all_initials.append(py[0].lower())

        except ImportError:
            pass

        # 去重
        unique_initials = list(set(all_initials))

        # 生成组合
        if len(unique_initials) >= 2:
            # 两个字母的组合
            for combo in iter_combinations(unique_initials, 2):
                mixed_combinations.add(''.join(combo))
                mixed_combinations.add(''.join(combo).upper())

            # 两个字母的排列
            for perm in iter_permutations(unique_initials, 2):
                mixed_combinations.add(''.join(perm))
                mixed_combinations.add(''.join(perm).upper())

        return mixed_combinations

    def run(self) -> Set[str]:
        """生成所有首字母组合"""
        all_combinations = set()

        # 英文名首字母
        if self.name_en:
            all_combinations.update(self.create_english_initials(self.name_en))

        # 英文昵称首字母
        if self.nickname_en:
            all_combinations.update(self.create_english_initials(self.nickname_en))  # noqa

        # 中文名首字母
        if self.name_zh:
            all_combinations.update(self.create_chinese_initials(self.name_zh))

        # 中文昵称首字母
        if self.nickname_zh:
            all_combinations.update(self.create_chinese_initials(self.nickname_zh))  # noqa

        # 混合首字母组合
        all_combinations.update(self.create_mixed_initials())

        # 过滤掉单个字符的组合
        return {combo for combo in all_combinations if len(combo) >= 2}
