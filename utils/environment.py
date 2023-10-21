import os


def get_env_variable(variable_name, default_value=''):
    return os.environ.get(variable_name, default_value)


def parse_comma_sep_str_to_list(comma_sep_str):
    # se nao for strings corretamente ele ja retorna uma lista vazia
    # se nao for uma instancia de strings ele retorna um lista vazia
    if not comma_sep_str or not isinstance(comma_sep_str, str):
        return []
    return [string.strip() for string in comma_sep_str.split(',') if string]


if __name__ == '__main__':
    print(parse_comma_sep_str_to_list(get_env_variable('ALLOWED_HOSTS')))
    print(parse_comma_sep_str_to_list(''))
    print(parse_comma_sep_str_to_list(123))
    print(parse_comma_sep_str_to_list('a, b, c'))
