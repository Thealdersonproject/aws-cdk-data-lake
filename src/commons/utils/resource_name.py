import re
from typing import AnyStr, List


def create_resource_name_regex(
        min_length: int = 3,
        max_length:int = 63,
        allowed_chars:str = r"a-z",
        separator:str = "-",
        allow_start_with_separator:bool = False,
        allow_end_with_separator:bool = False,
        allow_uppercase:bool = False,
        allow_numeric:bool = False,
    ) -> re.Pattern[AnyStr]:

    chars = allowed_chars
    if allow_numeric:
        chars += "0-9"

    if allow_uppercase:
        chars += "A-Z"

    start:str  = rf"[{separator}]?" if allow_start_with_separator else rf"[{chars}]"
    end:str  = rf"[{separator}]?" if allow_end_with_separator else rf"[{chars}]"
    middle:str  = rf"[{chars}{separator}]"

    pattern:str  = rf"^{start}{middle}{{{min_length - 2},{max_length - 2}}}{end}$"
    return re.compile(pattern)


def force_naming_pattern(
        input_string: str,
        regex_pattern: re.Pattern[AnyStr],
        separator:str = "-",
        allow_uppercase:bool = False
    ) -> str:

    allowed_chars:str = regex_pattern.pattern.split("]")[0][2:]
    cleaned_string:str = "".join(c for c in input_string if c in allowed_chars or c == separator)
    if not allow_uppercase:
        cleaned_string = cleaned_string.lower()

    cleaned_string = re.sub(rf"{separator}+", f"{separator}", cleaned_string)
    if not regex_pattern.match(f"{separator}{cleaned_string}"):
        cleaned_string = cleaned_string.strip(separator)

    max_length:int = int(regex_pattern.pattern.split(",")[-1].split("}")[0])
    if len(cleaned_string) > max_length:
        cleaned_string = cleaned_string[:max_length]
        if not regex_pattern.match(cleaned_string):
            cleaned_string = cleaned_string.rstrip(separator)

    min_length:int = int(regex_pattern.pattern.split(",")[-2].split("{")[-1])
    while len(cleaned_string) < min_length:
        cleaned_string += "a"

    return cleaned_string


def format_logical_name(
        logical_name: str,
        resource_name_allow_upper_case:bool,
        resource_name_forbidden_chars:List[str],
        resource_name_forbidden_start:List[str],
        resource_name_forbidden_end:List[str],
        resource_name_separator:str,
        resource_name_pattern:str,
        resource_name_forbidden_chars_new_value:str,
        resource_name_min_size:int = 3,
        resource_name_max_size:int = 63,
        allow_start_with_separator:bool = False,
        allow_end_with_separator:bool = False,
        resource_name_allow_numeric:bool = True,
        **kwargs
    ) -> str:

    resource_name: str = logical_name.strip()
    if not resource_name_allow_upper_case:
        resource_name = resource_name.lower()

    for clean_name in resource_name_forbidden_chars:
        resource_name = resource_name.replace(clean_name, f"{resource_name_forbidden_chars_new_value}")

    for clean_start in resource_name_forbidden_start:
        if resource_name.startswith(clean_start):
            resource_name = resource_name[len(clean_start):]

    for clean_end in resource_name_forbidden_end:
        if resource_name.endswith(clean_end):
            resource_name = resource_name[: len(clean_end)]

    resource_name = re.sub(rf"{resource_name_separator}+", f"{resource_name_separator}", resource_name)
    resource_name = re.sub(r"\s+", " ", resource_name)
    resource_name = resource_name.replace(" ", f"{resource_name_separator}")

    kwargs["resource_logical_name"] = resource_name
    resource_name = resource_name_pattern.format(**kwargs)

    resource_name_regex = create_resource_name_regex(
        min_length = resource_name_min_size,
        max_length = resource_name_max_size,
        allowed_chars = r"a-z",
        separator = "-",
        allow_start_with_separator = allow_start_with_separator,
        allow_end_with_separator = allow_end_with_separator,
        allow_uppercase = resource_name_allow_upper_case,
        allow_numeric = resource_name_allow_numeric,
    )

    resource_name = force_naming_pattern(
        input_string = resource_name,
        regex_pattern=resource_name_regex,
        separator=resource_name_separator,
        allow_uppercase=resource_name_allow_upper_case
    )

    return resource_name

