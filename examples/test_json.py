from src.main import compare_json

result = compare_json(
    "examples/first.json",
    "examples/second.json"
)

print("Результат сравнения:")
print(result)