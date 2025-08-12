from typing import Dict, Any, List
import json
import re
from .settings import (COMMON_SUFFIX, REGULAR_YEARS,  # type: ignore
                       VALID_SPECIAL_CHARS)


class CollectInput:
    """收集和验证个人信息输入"""

    def __init__(self, name_en: str = "", name_zh: str = "",
                 nickname_en: str = "", nickname_zh: str = "",
                 birthday: str = "", email: str = "",
                 phone: str = "", username: str = "",
                 company_en: str = "", company_zh: str = "",
                 department_en: str = "", department_zh: str = "",
                 special_chars: str = "",
                 common_suffix: List[str] = [],
                 regular_years: List[str] = []) -> None:
        self.name_en = name_en.strip()
        self.name_zh = name_zh.strip()
        self.nickname_en = nickname_en.strip()
        self.nickname_zh = nickname_zh.strip()
        self.birthday = birthday.strip()
        self.email = email.strip()
        self.phone = phone.strip()
        self.username = username.strip()
        self.company_en = company_en.strip()
        self.company_zh = company_zh.strip()
        self.department_en = department_en.strip()
        self.department_zh = department_zh.strip()
        self.special_chars = special_chars.strip()  # 用户输入的特殊字符
        self.common_suffix = common_suffix + COMMON_SUFFIX if common_suffix else COMMON_SUFFIX.copy()  # noqa
        self.regular_years = regular_years + REGULAR_YEARS if regular_years else REGULAR_YEARS.copy()  # noqa

    def validate_input(self) -> Dict[str, bool]:
        """验证输入数据的有效性"""
        validation_result = {
            'birthday': self._validate_birthday(),
            'email': self._validate_email(),
            'phone': self._validate_phone(),
            'special_chars': self._validate_special_chars(),
        }
        return validation_result

    def _validate_birthday(self) -> bool:
        """验证生日格式 (YYYY-MM-DD 或 YYYY/MM/DD)"""
        if not self.birthday:
            return True  # 空值也算有效

        patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{4}/\d{2}/\d{2}$',  # YYYY/MM/DD
            r'^\d{4}\d{2}\d{2}$',    # YYYYMMDD
            r'^\d{4}-\d{1,2}-\d{1,2}$',  # YYYY-M-D 或 YYYY-MM-D
            r'^\d{4}/\d{1,2}/\d{1,2}$',  # YYYY/M/D 或 YYYY/MM/D
        ]

        return any(re.match(pattern, self.birthday) for pattern in patterns)

    def _validate_email(self) -> bool:
        """验证邮箱格式"""
        if not self.email:
            return True

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.email) is not None

    def _validate_phone(self) -> bool:
        """验证手机号格式"""
        if not self.phone:
            return True

        # 支持中国手机号和国际格式
        patterns = [
            r'^1[3-9]\d{9}$',  # 中国手机号
            r'^\+\d{1,3}\d{7,14}$',  # 国际格式
            r'^\d{7,15}$',  # 通用格式
        ]

        return any(re.match(pattern, self.phone) for pattern in patterns)

    def _validate_special_chars(self) -> bool:
        """验证特殊字符"""
        if not self.special_chars:
            return True  # 允许为空

        # 检查是否包含有效的特殊字符
        return all(char in VALID_SPECIAL_CHARS or char.isalnum() or char.isspace() # noqa
                   for char in self.special_chars)

    def has_special_chars(self) -> bool:
        """检查是否有特殊字符"""
        return bool(self.special_chars.strip())

    def get_special_chars_list(self) -> List[str]:
        """获取特殊字符列表"""
        if not self.special_chars:
            return []
        # 去重并保持顺序
        seen = set()
        result = []
        for char in self.special_chars:
            if char not in seen and not char.isspace():
                seen.add(char)
                result.append(char)
        return result

    def add_custom_affix(self, affix: str) -> None:
        """添加自定义后缀/前缀"""
        if affix and affix not in self.common_suffix:
            self.common_suffix.append(affix)

    def add_custom_year(self, year: str) -> None:
        """添加自定义年份"""
        if year and year not in self.regular_years:
            self.regular_years.append(year)

    def set_special_chars(self, special_chars: str) -> bool:
        """设置特殊字符并验证"""
        self.special_chars = special_chars.strip()
        return self._validate_special_chars()

    def get_birth_year(self) -> str:
        """获取出生年份"""
        if self.birthday:
            # 提取年份
            year_match = re.match(r'^(\d{4})', self.birthday)
            if year_match:
                return year_match.group(1)
        return ""

    def get_birth_parts(self) -> Dict[str, str]:
        """获取生日各部分"""
        parts = {'year': '', 'month': '', 'day': '', 'all': ''}

        if self.birthday:
            # 提取数字
            digits = re.findall(r'\d+', self.birthday)
            if len(digits) >= 3:
                parts['all'] = ''.join(digits)
                parts['year'] = digits[0]
                parts['month'] = digits[1].zfill(2)  # 补齐两位
                parts['day'] = digits[2].zfill(2)    # 补齐两位

        return parts

    def get_phone_parts(self) -> Dict[str, str]:
        """获取手机号各部分"""
        parts = {'last4': '', 'all_digits': ''}

        if self.phone:
            digits = re.findall(r'\d', self.phone)
            all_digits = ''.join(digits)
            parts['all_digits'] = all_digits

            if len(digits) >= 4:
                parts['last4'] = ''.join(digits[-4:])

        return parts

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'name_en': self.name_en,
            'name_zh': self.name_zh,
            'nickname_en': self.nickname_en,
            'nickname_zh': self.nickname_zh,
            'birthday': self.birthday,
            'email': self.email,
            'phone': self.phone,
            'username': self.username,
            'company_en': self.company_en,
            'company_zh': self.company_zh,
            'department_en': self.department_en,
            'department_zh': self.department_zh,
            'special_chars': self.special_chars,
            'common_suffix': self.common_suffix,
            'regular_years': self.regular_years,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CollectInput':
        """从字典创建实例"""
        return cls(**data)

    @classmethod
    def from_json_file(cls, file_path: str) -> 'CollectInput':
        """从JSON文件加载"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def save_to_json(self, file_path: str) -> None:
        """保存到JSON文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    def get_all_names(self) -> List[str]:
        """获取所有名字相关信息"""
        names = []
        if self.name_en:
            names.append(self.name_en)
        if self.name_zh:
            names.append(self.name_zh)
        if self.nickname_en:
            names.append(self.nickname_en)
        if self.nickname_zh:
            names.append(self.nickname_zh)
        if self.username:
            names.append(self.username)
        return names

    def get_all_organizations(self) -> List[str]:
        """获取所有组织相关信息"""
        orgs = []
        if self.company_en:
            orgs.append(self.company_en)
        if self.company_zh:
            orgs.append(self.company_zh)
        if self.department_en:
            orgs.append(self.department_en)
        if self.department_zh:
            orgs.append(self.department_zh)
        return orgs

    def get_email_username(self) -> str:
        """获取邮箱用户名部分"""
        if self.email and '@' in self.email:
            return self.email.split('@')[0]
        return ""

    def get_email_domain(self) -> str:
        """获取邮箱域名部分"""
        if self.email and '@' in self.email:
            return self.email.split('@')[1]
        return ""

    def is_empty(self) -> bool:
        """检查是否为空信息"""
        fields = [
            self.name_en, self.name_zh, self.nickname_en, self.nickname_zh,
            self.birthday, self.email, self.phone, self.username,
            self.company_en, self.company_zh,
            self.department_en, self.department_zh
        ]
        return not any(field.strip() for field in fields)

    def get_summary(self) -> str:
        """获取信息摘要"""
        summary_parts = []

        if self.name_zh or self.name_en:
            name = self.name_zh or self.name_en
            summary_parts.append(f"姓名: {name}")

        if self.birthday:
            summary_parts.append(f"生日: {self.birthday}")

        if self.company_zh or self.company_en:
            company = self.company_zh or self.company_en
            summary_parts.append(f"公司: {company}")

        if self.email:
            summary_parts.append(f"邮箱: {self.email}")

        if self.phone:
            summary_parts.append(f"手机: {self.phone}")

        if self.special_chars:
            summary_parts.append(f"特殊字符: {self.special_chars}")

        return " | ".join(summary_parts) if summary_parts else "无信息"
