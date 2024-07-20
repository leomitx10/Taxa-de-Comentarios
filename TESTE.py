import subprocess
import json
import os

project_path = os.path.expanduser('~/Área de Trabalho/gecko-dev')

def count_directories(path):
    total_dirs = 0
    for _, dirs, _ in os.walk(path):
        total_dirs += len(dirs)
    return total_dirs

try:
    result = subprocess.run(['cloc', '--json', '--include-lang=C,Kotlin,PHP,Rust,C++,JavaScript', project_path],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=18000)
    cloc_output = result.stdout.decode('utf-8')
    error_output = result.stderr.decode('utf-8')
    
    if error_output:
        print("Erros encontrados durante a execução do cloc:")
        print(error_output)
    
    cloc_data = json.loads(cloc_output)
    
    def comment_rate(language_data):
        comment_lines = language_data.get('comment', 0)
        code_lines = language_data.get('code', 0)
        if code_lines == 0:
            return 0
        return comment_lines / code_lines
    
    def weighted_comment_rate(data, languages):
        total_comments = 0
        total_code_lines = 0
        for lang in languages:
            lang_data = data.get(lang, {})
            comments = lang_data.get('comment', 0)
            code_lines = lang_data.get('code', 0)
            total_comments += comments
            total_code_lines += code_lines
        if total_code_lines == 0:
            return 0
        return total_comments / total_code_lines
    
    # Calcular a porcentagem ponderada de comentários para C, Kotlin, PHP, Rust, C++ e JavaScript
    languages = ['C', 'Kotlin', 'PHP', 'Rust', 'C++', 'JavaScript']
    overall_comment_rate = weighted_comment_rate(cloc_data, languages)
    
    print(f"Taxa geral de comentários: {overall_comment_rate:.2%}")
    
    # Contar o número de arquivos e linhas analisadas
    total_files = cloc_data.get('header', {}).get('n_files', 0)
    total_lines = cloc_data.get('header', {}).get('n_lines', 0)
    
    # Contar o número de pastas analisadas
    total_directories = count_directories(project_path)
    
    print(f"Número total de arquivos analisados: {total_files}")
    print(f"Número total de linhas analisadas: {total_lines}")
    print(f"Número total de pastas analisadas: {total_directories}")

except subprocess.TimeoutExpired:
    print("O comando `cloc` excedeu o tempo limite de 5 horas.")
except json.JSONDecodeError:
    print("Erro ao analisar a saída JSON do cloc.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
