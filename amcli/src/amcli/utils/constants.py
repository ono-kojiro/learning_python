# amcli/utils/constants.py
from enum import Enum

class FieldType(str, Enum):
    FOREIGN_KEY = "ForeignKey"
    ONE_TO_ONE = "OneToOneField"
    MANY_TO_MANY = "ManyToManyField"

    CHAR = "CharField"
    TEXT = "TextField"
    INTEGER = "IntegerField"
    FLOAT = "FloatField"
    BOOLEAN = "BooleanField"
    JSON = "JSONField"

    # ★ 追加: 日付・日時フィールド
    DATETIME = "DateTimeField"
    DATE = "DateField"


def normalize_field_type(ftype: str) -> FieldType:
    """
    JSON から読み込んだフィールドタイプ文字列を FieldType Enum に変換する。
    typo があれば即エラーになるので安全。
    """
    try:
        return FieldType(ftype)
    except ValueError:
        raise ValueError(f"Unknown field type: {ftype}")
