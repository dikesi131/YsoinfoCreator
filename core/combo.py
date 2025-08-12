import re
from typing import Set, List, Dict
from .collect_input import CollectInput  # type: ignore
from .create_name_pinyin import NamePinyinCreator  # type: ignore
from .create_name_initial import NameInitialCreator  # type: ignore
from .settings import (COMMON_PREFIX, COMMON_SEPARATORS,  # type: ignore
                       TOP_100_COMMON_PASSWORDS)


class Combo:
    """生成基于个人信息的用户名和密码组合"""

    def __init__(self) -> None:
        self.common_separators = COMMON_SEPARATORS

    def generate_usernames(self, personal_info: CollectInput) -> Set[str]:
        """生成用户名组合"""
        usernames = set()

        # 使用个人信息中的自定义后缀
        suffixes_to_use = personal_info.common_suffix

        # 使用个人信息中的自定义年份
        years_to_use = personal_info.regular_years

        # 基础名字组合
        base_names = self._get_base_names(personal_info)

        # 1. 直接使用名字
        usernames.update(base_names)

        # 2. 名字 + 后缀
        for name in base_names:
            for suffix in suffixes_to_use:
                usernames.add(name + suffix)

        # 3. 名字 + 年份
        for name in base_names:
            for year in years_to_use:
                usernames.add(name + year)
                usernames.add(year + name)

        # 4. 前缀(常见用户名)
        for prefix in COMMON_PREFIX:
            usernames.add(prefix)

        # 5. 前缀(常见用户名) + 名字 or 名字 + 前缀
        for name in base_names:
            for prefix in COMMON_PREFIX:
                usernames.add(prefix + name)
                usernames.add(name + prefix)

        # 6. 前缀(常见用户名) + 后缀
        for prefix in COMMON_PREFIX:
            for suffix in suffixes_to_use:
                usernames.add(prefix + suffix)

        # 7. 前缀(常见用户名) + 年份
        for prefix in COMMON_PREFIX:
            for year in years_to_use:
                usernames.add(prefix + year)

        # 8. 基于生日的组合
        if personal_info.birthday:
            birth_parts = personal_info.get_birth_parts()
            for name in base_names:
                # 使用生日的各个部分
                for _, part_value in birth_parts.items():
                    if part_value:
                        usernames.add(name + part_value)
                        usernames.add(part_value + name)

        # 9. 基于公司的组合
        company_parts = self._get_company_parts(personal_info)
        for name in base_names:
            for company in company_parts:
                for sep in self.common_separators:
                    if sep:  # 不为空字符串时
                        usernames.add(name + sep + company)
                        usernames.add(company + sep + name)

        # 10. 基于邮箱的组合
        if personal_info.email:
            # example: test@qq.com -> test
            email_username = personal_info.email.split('@')[0]
            usernames.add(email_username)

            # email_username + common suffix
            for suffix in suffixes_to_use:
                usernames.add(email_username + suffix)

        # 11. 基于手机号的组合
        if personal_info.phone:
            phone_parts = self._extract_phone_parts(personal_info.phone)
            for name in base_names:
                for part in phone_parts:
                    usernames.add(name + part)
                    usernames.add(part + name)

        return self._filter_usernames(usernames)

    def generate_passwords(self, personal_info: CollectInput) -> Set[str]:
        """生成密码组合"""
        passwords = set()

        # 使用个人信息中的自定义设置
        suffixes_to_use = personal_info.common_suffix
        years_to_use = personal_info.regular_years
        if personal_info.special_chars:
            special_chars = personal_info.special_chars
            separators_to_use = COMMON_SEPARATORS + list(special_chars)
        else:
            separators_to_use = COMMON_SEPARATORS

        # 基础名字
        base_names = self._get_base_names(personal_info)

        # 获取生日和手机号信息
        birth_parts = personal_info.get_birth_parts()
        phone_parts = personal_info.get_phone_parts()

        # 公司名
        company_names = self._get_company_parts(personal_info)

        # 1. 基础名字 + 后缀
        for name in base_names:
            for suffix in suffixes_to_use:
                passwords.add(name + suffix)

        # 2. 基础名字 + 特殊字符 + 后缀
        for name in base_names:
            for suffix in suffixes_to_use:
                for sep in separators_to_use:
                    passwords.add(name + sep + suffix)

        # 3. 基础名字 + 年份
        for name in base_names:
            for year in years_to_use:
                passwords.add(name + year)
                passwords.add(year + name)

        # 4. 基础名字 + 特殊字符 + 年份
        for name in base_names:
            for year in years_to_use:
                for sep in separators_to_use:
                    passwords.add(name + sep + year)
                    passwords.add(year + sep + name)

        # 5. 前缀 + 后缀
        for prefix in COMMON_PREFIX:
            for suffix in suffixes_to_use:
                passwords.add(prefix + suffix)

        # 6. 前缀 + 特殊字符 + 后缀
        for prefix in COMMON_PREFIX:
            for suffix in suffixes_to_use:
                for sep in separators_to_use:
                    passwords.add(prefix + sep + suffix)

        # 7. 前缀 + 年份
        for prefix in COMMON_PREFIX:
            for year in years_to_use:
                passwords.add(prefix + year)

        # 8. 前缀 + 特殊字符 + 年份
        for prefix in COMMON_PREFIX:
            for year in years_to_use:
                for sep in separators_to_use:
                    passwords.add(prefix + sep + year)

        # 9. 基于生日的组合
        for name in base_names:
            for part in birth_parts.values():
                if part:
                    passwords.add(name + part)
                    for sep in separators_to_use:
                        passwords.add(name + sep + part)

        # 10. 基于手机号的组合
        for name in base_names:
            for part in phone_parts.values():
                if part:
                    passwords.add(name + part)
                    for sep in separators_to_use:
                        passwords.add(name + sep + part)

        # 11. 公司名相关组合
        for name in base_names:
            for company in company_names:
                for sep in self.common_separators:
                    if sep:
                        passwords.add(name + sep + company)
                        passwords.add(company + sep + name)

        # 12. 常见密码
        passwords.update(TOP_100_COMMON_PASSWORDS)

        return self._filter_passwords(passwords)

    def _get_base_names(self, personal_info: CollectInput) -> Set[str]:
        """获取基础名字集合"""
        names = set()

        # 直接的名字
        if personal_info.name_en:
            # lower + capitalize
            names.add(personal_info.name_en.lower())
            names.add(personal_info.name_en.capitalize())
            names.update(self._split_english_name(personal_info.name_en))

        if personal_info.nickname_en:
            # lower + capitalize
            names.add(personal_info.nickname_en.lower())
            names.add(personal_info.nickname_en.capitalize())

        if personal_info.username:
            # lower + capitalize
            names.add(personal_info.username.lower())
            names.add(personal_info.username.capitalize())

        # 中文名的拼音
        if personal_info.name_zh:
            try:
                pinyin_creator = NamePinyinCreator(personal_info.name_zh,
                                                   personal_info.nickname_zh)
                names.update(pinyin_creator.run())
            except Exception as e:
                print(f"⚠️ 拼音生成警告: {e}")

        # 首字母组合
        try:
            initial_creator = NameInitialCreator(
                personal_info.name_zh,
                personal_info.name_en,
                personal_info.nickname_zh,
                personal_info.nickname_en
            )
            names.update(initial_creator.run())
        except Exception as e:
            print(f"⚠️ 首字母组合生成警告: {e}")

        return names

    def _split_english_name(self, name: str) -> Set[str]:
        """分解英文名"""
        names = set()
        clean_name = re.sub(r'[^a-zA-Z\s]', '', name)
        words = clean_name.lower().split()

        for word in words:
            if len(word) >= 2:
                names.add(word)

        return names

    def _extract_birthday_parts(self, birthday: str) -> List[str]:
        """提取生日相关信息"""
        parts = []

        # 提取数字
        digits = re.findall(r'\d+', birthday)

        for digit in digits:
            if len(digit) == 4:  # 年份
                parts.append(digit)
                parts.append(digit[2:])  # 年份后两位
            elif len(digit) == 2:  # 月份或日期
                parts.append(digit)

        # 常见生日格式
        if len(digits) >= 3:
            year, month, day = digits[0], digits[1], digits[2]
            parts.extend([
                month + day,  # 月日
                day + month,  # 日月
                year[2:] + month + day,  # 年月日 (后两位年份)
            ])

        return parts

    def _get_company_parts(self, personal_info: CollectInput) -> List[str]:
        """获取公司相关信息"""
        parts: List[str] = []

        if personal_info.company_en:
            clean_company = re.sub(r'[^a-zA-Z\s]', '',
                                   personal_info.company_en)
            words = clean_company.lower().split()
            parts.extend(word for word in words if len(word) >= 2)

        if personal_info.company_zh:
            company_pinyin = NamePinyinCreator(name_zh=personal_info.company_zh).run()  # noqa
            company_initial = NameInitialCreator(name_zh=personal_info.company_zh).run()  # noqa
            parts.extend(list(company_pinyin))
            parts.extend(list(company_initial))

        if personal_info.department_en:
            clean_dept = re.sub(r'[^a-zA-Z\s]', '',
                                personal_info.department_en)
            words = clean_dept.lower().split()
            parts.extend(word for word in words if len(word) >= 2)

        return parts

    def _extract_phone_parts(self, phone: str) -> List[str]:
        """提取手机号相关信息"""
        parts = []
        digits = re.findall(r'\d', phone)

        if len(digits) >= 4:
            # 后四位
            parts.append(''.join(digits[-4:]))

            # 后六位
            if len(digits) >= 6:
                parts.append(''.join(digits[-6:]))

            # 中间四位 (如果是11位手机号)
            if len(digits) == 11:
                parts.append(''.join(digits[3:7]))

        return parts

    def _filter_usernames(self, usernames: Set[str]) -> Set[str]:
        """过滤用户名"""
        filtered = set()
        min_length = 3
        max_length = 20

        for username in usernames:
            # 清理字符串
            clean = username.strip().lower()

            # 长度检查
            if min_length <= len(clean) <= max_length:
                filtered.add(clean)

        return filtered

    def _filter_passwords(self, passwords: Set[str]) -> Set[str]:
        """过滤密码"""
        filtered = set()
        min_length = 4

        for password in passwords:
            # 长度检查
            if len(password) >= min_length:
                # 去掉明显无效的组合
                if not password.isspace() and password.strip():
                    filtered.add(password.strip())

        return filtered

    def generate_all_combinations(self, personal_info: CollectInput) -> Dict[str, Set[str]]:  # noqa
        """生成所有组合"""
        return {
            'usernames': self.generate_usernames(personal_info),
            'passwords': self.generate_passwords(personal_info)
        }
