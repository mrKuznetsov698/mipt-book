#!/usr/bin/env python3
"""Проверка номеров задач и геометрии билетов в готовом PDF (PyMuPDF)."""
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
assert len(document) == len(source_pages) == 19, "Нарушены границы страниц"
assert len(exercises) == 244, "Не все задачи прочитаны из исходника"
all_numbers = []
ticket_count = 0

for page, (printed_page, body) in zip(document, source_pages):
    number = int(printed_page)
    expected = list(map(int, re.findall(r"\\begin\{TrigExercise\}\{(\d+)\}", body)))
    actual = list(map(int, re.findall(r"\b2\.(\d+)\.", page.get_text())))
    assert actual == expected, f"Страница {number}: изменились номера задач"
    all_numbers.extend(actual)
    spans = [
        span
        for block in page.get_text("dict")["blocks"]
        for line in block.get("lines", [])
        for span in line["spans"]
    ]
    headings = [s for s in spans if re.fullmatch(r"2\.\d+\.", s["text"].strip())]
    tickets = [s for s in spans if "(Билет" in s["text"]]
    assert len(headings) == len(tickets) == len(expected), f"Страница {number}: потерян билет"
    right = page.rect.width - (11 if number % 2 else 14) * 72 / 25.4

    for index, (exercise, heading, ticket) in enumerate(zip(expected, headings, tickets)):
        ticket_number, year = exercises[exercise]
        assert ticket["text"].strip() == f"(Билет {ticket_number}, {year})", f"2.{exercise}: неверная подпись"
        assert abs(ticket["bbox"][2] - right) < 0.1, f"2.{exercise}: билет смещён по горизонтали"
        assert ticket["bbox"][1] > heading["bbox"][3], f"2.{exercise}: билет выше формулы"
        end = headings[index + 1]["bbox"][1] if index + 1 < len(headings) else page.rect.height - 30
        assert ticket["bbox"][3] < end, f"2.{exercise}: билет попал в следующую задачу"
        if exercise in with_continuation:
            continuation = [
                s for s in spans
                if heading["bbox"][1] < s["bbox"][1] < end
                and s["text"].startswith(("принадлеж", "удовлетворяющие", "Найти:"))
            ]
            assert len(continuation) == 1, f"2.{exercise}: не найдено продолжение условия"
            assert ticket["origin"][1] < continuation[0]["origin"][1] - 2, f"2.{exercise}: билет привязан к тексту после формулы"
        ticket_count += 1

    if number in (31, 32):
        first_lines = page.search_for("Найти наименьшее натуральное число")
        second_lines = page.search_for("при котором выполняется равенство")
        assert len(first_lines) == len(second_lines)
        for first, second in zip(first_lines, second_lines):
            assert abs(first.x0 - second.x0) < 0.1, "Продолжение условия не выровнено"
        assert "выполня-" not in page.get_text(), "Остался перенос внутри слова"

assert all_numbers == list(range(1, 245)), "Нарушен порядок задач"
log = root / "main.log"
if log.exists():
    assert not re.search(r"Overfull|Underfull|Missing character", log.read_text()), "Есть предупреждения о вёрстке"
print(f"Проверено: {len(document)} страниц, {len(all_numbers)} задач, {ticket_count} билетов; подписи после формул не сдвигаются к продолжению условия.")
