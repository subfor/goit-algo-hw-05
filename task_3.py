import timeit
from pathlib import Path

import chardet


# Алгоритм  Боєра-Мура
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1


# Алгоритм  Кнута-Морріса-Пратта


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено


# Алгоритм  Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)

    # Базове число для хешування та модуль
    base = 256
    modulus = 101

    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus

    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i : i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (
                current_slice_hash - ord(main_string[i]) * h_multiplier
            ) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(main_string[i + substring_length])
            ) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def read_text_with_detect(path: Path) -> str:
    raw = path.read_bytes()
    enc = (chardet.detect(raw) or {}).get("encoding") or "utf-8"
    attempts = [enc, "utf-8", "cp1251", "latin-1"]
    for e in attempts:
        try:
            return raw.decode(e)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Не вдалося декодувати {path}")


ARTICLES = {
    "article1": Path("1.txt"),
    "article2": Path("2.txt"),
}
ALGORITHMS = [
    ("Boyer-Moore", boyer_moore_search),
    ("KMP", kmp_search),
    ("Rabin-Karp", rabin_karp_search),
]
PATTERNS = {
    # "ключ": ("ключ_тексту", "підрядок")
    "exists": ("article1", "Алгоритм"),
    "no_exists": ("article1", "QWERTYUIOP"),
    "exists2": ("article2", "Алгоритм"),
    "no_exists2": ("article2", "QWERTYUIOP"),
}

TEXTS = {key: read_text_with_detect(p) for key, p in ARTICLES.items()}


def bench():
    results = []
    for alg_name, alg_func in ALGORITHMS:
        for patt_key, (txt_key, patt) in PATTERNS.items():
            text = TEXTS[txt_key]
            stmt = lambda t=text, p=patt, fn=alg_func: fn(t, p)
            timer = timeit.Timer(stmt=stmt)
            best_time = min(timer.repeat(repeat=5, number=1))
            results.append(
                {
                    "algorithm": alg_name,
                    "text": txt_key,
                    "pattern": patt_key,
                    "time_sec": best_time,
                }
            )
    return results


def show_rezults(rows):
    print("\nResults\n" + "-" * 40)
    print(
        "{:<12} {:<10} {:<8} {:>10}".format("Algorithm", "Text", "Pattern", "Time, s")
    )
    for r in rows:
        print(
            "{:<12} {:<10} {:<10} {:>10.6f}".format(
                r["algorithm"], r["text"], r["pattern"], r["time_sec"]
            )
        )
    print("-" * 40)


def summarize(rows):
    totals_per_text, totals_overall = {}, {}

    for rezult in rows:
        algo, text, t = rezult["algorithm"], rezult["text"], rezult["time_sec"]

        # сумуємо по текстах
        totals_per_text.setdefault(text, {}).setdefault(algo, 0.0)
        totals_per_text[text][algo] += t

        # сумуємо загалом
        totals_overall.setdefault(algo, 0.0)
        totals_overall[algo] += t

    fast_per_text = {
        text: min(times, key=times.get)  # алгоритм із мінімальним часом
        for text, times in totals_per_text.items()
    }
    fastest_overall = min(totals_overall, key=totals_overall.get)

    return fast_per_text, fastest_overall, totals_per_text, totals_overall


def print_summary(fast_per_text, fastest_overall):
    print("\nНайшвидші алгоритми:")
    for text, algo in fast_per_text.items():
        print(f"  • {text}: {algo}")
    print(f"  • У цілому: {fastest_overall}\n")


if __name__ == "__main__":
    result_rows = bench()
    show_rezults(result_rows)
    fast_txt, fast_all, *_ = summarize(result_rows)
    print_summary(fast_txt, fast_all)
