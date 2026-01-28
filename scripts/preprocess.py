import pandas as pd

# Func to translate column names from English to Portuguese
def rename_columns(df):
    translate_columns = {
        'work_year': 'ano',
        'experience_level': 'senioridade',
        'employment_type': 'contrato',
        'job_title': 'cargo',
        'salary': 'salario',
        'salary_currency': 'moeda',
        'salary_in_usd': 'salario_usd',
        'employee_residence': 'residencia',
        'remote_ratio': 'remoto',
        'company_location': 'empresa',
        'company_size': 'tamanho_empresa',
    }
    return df.rename(columns=translate_columns)

# Func to translate/rename column values from English to Portuguese
def translate_values(df):
    df["contrato"] = df["contrato"].replace({
        'FT': 'Tempo Integral',
        'CT': 'Contrato',
        'PT': 'Meio Período',
        'FL': 'Freelancer'
    })
    df["tamanho_empresa"] = df["tamanho_empresa"].replace({
        'M': 'Média',
        'L': 'Grande',
        'S': 'Pequena'
    })
    df["senioridade"] = df["senioridade"].replace({
        'SE': 'Senior',
        'MI': 'Pleno',
        'EN': 'Junior',
        'EX': 'Executivo'
    })
    df["remoto"] = df["remoto"].replace({
        0: 'Presencial',
        50: 'Híbrido',
        100: 'Remoto'
    })
    return df

# Preprocess Function
def preprocess(df):
    df = rename_columns(df)
    df = translate_values(df)
    return df