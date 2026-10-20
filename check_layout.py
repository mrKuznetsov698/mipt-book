#!/usr/bin/env python3
"""Проверка задач и билетов в двухколоночном A4 и в книжном формате."""
from pathlib import Path
import re
import sys

import fitz

root = Path(__file__).resolve().parent
source = (root / "trigonometry.tex").read_text()
pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "trigonometry.pdf"
document = fitz.open(pdf_path)
source_pages = re.findall(
    r"\\begin\{TrigSourcePage\}\{(\d+)\}(.*?)\\end\{TrigSourcePage\}",
    source, re.S,
)
exercises = {
    int(number): (int(ticket), year)
    for number, ticket, year in re.findall(
        r"\\begin\{TrigExercise\}\{(\d+)\}\{[^\n]*\}\{(\d+)\}\{(\d{4})\}",
        source,
    )
}
with_continuation = set(range(17, 21)) | set(range(49, 53)) | set(range(193, 197)) | set(range(225, 229))
landscape = document[0].rect.width > document[0].rect.height
assert len(source_pages) == 19 and len(exercises) == 244, "Не все задачи прочитаны из исходника"
if not landscape:
    assert len(document) == 19, "Нарушены границы книжных страниц"
all_numbers = []
ticket_count = 0
wrapped_headings = 0
mm = 72 / 25.4

for page_index, page in enumerate(document):
    spans = [
        span
        for block in page.get_text("dict")["blocks"]
        for line in block.get("lines", [])
        for span in line["spans"]
    ]
    assert "\ufffd" not in page.get_text(), "В PDF есть нераспознанные символы"
    page_numbers = []
    columns = 2 if landscape else 1
    for column in range(columns):
        column_spans = [s for s in spans if not landscape or (s["bbox"][0] < page.rect.width / 2) == (column == 0)]
        headings = sorted(
            [s for s in column_spans if re.fullmatch(r"2\.\d+\.", s["text"].strip())],
            key=lambda s: s["origin"][1],
        )
        tickets = sorted(
            [s for s in column_spans if "(Билет" in s["text"]],
            key=lambda s: s["origin"][1],
        )
        assert len(headings) == len(tickets), f"Страница {page_index + 1}, колонка {column + 1}: потерян билет"
        if landscape:
            column_width = (page.rect.width - 40 * mm) / 2
            right = 10 * mm + column_width if column == 0 else page.rect.width - 10 * mm
        else:
            printed_page = int(source_pages[page_index][0])
            right = page.rect.width - (11 if printed_page % 2 else 14) * mm

        for index, (heading, ticket) in enumerate(zip(headings, tickets)):
            exercise = int(heading["text"].strip().split(".")[1])
            page_numbers.append(exercise)
            ticket_number, year = exercises[exercise]
            assert ticket["text"].strip() == f"(Билет {ticket_number}, {year})", f"2.{exercise}: неверная подпись"
            assert abs(ticket["bbox"][2] - right) < 0.1, f"2.{exercise}: билет смещён по горизонтали"
            assert ticket["bbox"][1] > heading["bbox"][3], f"2.{exercise}: билет выше формулы"
            end = headings[index + 1]["bbox"][1] if index + 1 < len(headings) else page.rect.height - 30
            assert ticket["bbox"][3] < end, f"2.{exercise}: билет попал в следующую задачу"
            if exercise in with_continuation:
                continuation = [
                    s for s in column_spans
                    if heading["bbox"][1] < s["bbox"][1] < end
                    and s["text"].lstrip().startswith(("принадлеж", "удовлетворяющие", "Найти:"))
                ]
                assert len(continuation) == 1, f"2.{exercise}: не найдено продолжение условия"
                assert ticket["origin"][1] < continuation[0]["origin"][1] - 2, f"2.{exercise}: билет привязан к тексту после формулы"
            ticket_count += 1

    assert page_numbers, f"Страница {page_index + 1}: пустая страница"
    all_numbers.extend(page_numbers)
    if not landscape:
        expected = list(map(int, re.findall(r"\\begin\{TrigExercise\}\{(\d+)\}", source_pages[page_index][1])))
        assert page_numbers == expected, "Нарушено распределение задач по книжным страницам"
    first_lines = sorted(page.search_for("Найти наименьшее натуральное число"), key=lambda r: (r.x0, r.y0))
    second_lines = sorted(page.search_for("при котором выполняется равенство"), key=lambda r: (r.x0, r.y0))
    assert len(first_lines) == len(second_lines), "Утеряно продолжение условия 2.37–2.40"
    for first, second in zip(first_lines, second_lines):
        assert abs(first.x0 - second.x0) < 0.1, "Продолжение условия не выровнено"
        wrapped_headings += 1
    assert "выполня-" not in page.get_text(), "Остался перенос внутри слова"

assert all_numbers == list(range(1, 245)), "Нарушен порядок задач между страницами или колонками"
assert wrapped_headings == 4, "Не все четыре длинных условия проверены"
log = root / "main.log"
if log.exists():
    assert not re.search(r"Overfull|Underfull|Missing character|No hyphenation patterns", log.read_text()), "Есть предупреждения о вёрстке или локализации"
print(f"Проверено: {len(document)} страниц, 244 задачи, {ticket_count} билетов; локализация и продолжения условий без предупреждений.")
