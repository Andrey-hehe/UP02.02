import argparse
import difflib
import json
from pathlib import Path


def read_file(file_path):
    """Читает файл и возвращает его содержимое."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    content = path.read_text(encoding="utf-8")

    if path.suffix.lower() == ".json":
        data = json.loads(content)
        content = json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)

    return content


def get_changes(first_file, second_file):
    """Определяет добавленные, удалённые и изменённые строки."""
    first_lines = read_file(first_file).splitlines()
    second_lines = read_file(second_file).splitlines()

    matcher = difflib.SequenceMatcher(None, first_lines, second_lines)

    changes = {"added": [], "deleted": [], "modified": []}

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "insert":
            changes["added"].extend(second_lines[j1:j2])

        elif tag == "delete":
            changes["deleted"].extend(first_lines[i1:i2])

        elif tag == "replace":
            changes["modified"].append(
                {"old": first_lines[i1:i2], "new": second_lines[j1:j2]}
            )

    return changes


def compare_json(first_file, second_file):
    """Сравнивает два JSON-файла по отдельным полям."""
    first_data = json.loads(read_file(first_file))
    second_data = json.loads(read_file(second_file))

    if not isinstance(first_data, dict) or not isinstance(second_data, dict):
        raise TypeError("Корнем JSON должны быть объекты")

    changes = {"added": {}, "deleted": {}, "modified": {}}

    def compare_objects(old, new, prefix=""):
        for key in old.keys() | new.keys():
            path = f"{prefix}.{key}" if prefix else key

            if key not in old:
                changes["added"][path] = new[key]

            elif key not in new:
                changes["deleted"][path] = old[key]

            elif isinstance(old[key], dict) and isinstance(new[key], dict):
                compare_objects(old[key], new[key], path)

            elif old[key] != new[key]:
                changes["modified"][path] = {"old": old[key], "new": new[key]}

    compare_objects(first_data, second_data)

    return changes


def compare_files(first_file, second_file):
    """Создаёт HTML-отчёт о различиях двух файлов."""
    first_content = read_file(first_file)
    second_content = read_file(second_file)

    diff = difflib.HtmlDiff().make_file(
        first_content.splitlines(),
        second_content.splitlines(),
        fromdesc=Path(first_file).name,
        todesc=Path(second_file).name,
        charset="utf-8",
    )

    return diff


def save_report(html_report, output_file):
    """Сохраняет HTML-отчёт."""
    Path(output_file).write_text(html_report, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Модуль сравнения файлов")

    parser.add_argument("first_file", help="Первый файл")
    parser.add_argument("second_file", help="Второй файл")
    parser.add_argument("-o", "--output", default="report.html", help="Имя HTML-отчёта")

    args = parser.parse_args()

    try:
        report = compare_files(args.first_file, args.second_file)
        save_report(report, args.output)
        print(f"Отчёт успешно создан: {args.output}")

    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
