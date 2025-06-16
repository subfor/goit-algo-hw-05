## Результати вимірювань

| Алгоритм     | Текст     | Підрядок    | Час, с   |
|--------------|-----------|-------------|----------|
| Boyer-Moore  | article1  | exists      | 0.000064 |
| Boyer-Moore  | article1  | no_exists   | 0.000308 |
| Boyer-Moore  | article2  | exists2     | 0.000693 |
| Boyer-Moore  | article2  | no_exists2  | 0.000438 |
| KMP          | article1  | exists      | 0.000130 |
| KMP          | article1  | no_exists   | 0.000845 |
| KMP          | article2  | exists2     | 0.001462 |
| KMP          | article2  | no_exists2  | 0.001167 |
| Rabin–Karp   | article1  | exists      | 0.000215 |
| Rabin–Karp   | article1  | no_exists   | 0.002796 |
| Rabin–Karp   | article2  | exists2     | 0.003987 |
| Rabin–Karp   | article2  | no_exists2  | 0.003979 |

## Висновок

- **Boyer-Moore** показав найкращий час для обох текстів і загалом.  
- **KMP** в середньому у 2–3 рази повільніший.  
- **Rabin–Karp** — найповільніший (до 10 разів повільніший за Boyer-Moore).

> Якщо потрібен швидкий одноразовий пошук підрядка в тексті, варто обирати **алгоритм Бойєра-Мура**.
