import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import textwrap

max_width = 55 #character count until you get a \n

class FlashCard:
    def __init__(self, front, phonetic, translation, sentence, sentence_translation):
        self.front = front
        self.phonetic = phonetic
        self.translation = translation
        self.sentence = sentence
        self.sentence_translation = sentence_translation

def read_flashcards_from_csv(filename):
    flashcards = []
    with open(filename, 'r') as file:
        dialect = csv.Sniffer().sniff(file.read())
        file.seek(0)  # reset file pointer to beginning
        reader = csv.reader(file, dialect)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) != 5:
                print(f"Skipping row with {len(row)} columns: {row}")
                continue
            flashcards.append(FlashCard(*row))
    return flashcards

def replace_special_characters(flashcard):
    flashcard.front = flashcard.front.replace("\\n", "\n")
    flashcard.front = flashcard.front.replace("\"", "")
    flashcard.phonetic = flashcard.phonetic.replace("\\n", "\n")
    flashcard.phonetic = flashcard.phonetic.replace("\"", "")
    flashcard.translation = flashcard.translation.replace("\\n", "\n")
    flashcard.translation = flashcard.translation.replace("\"", "")
    flashcard.sentence = flashcard.sentence.replace("\\n", "\n")
    flashcard.sentence = flashcard.sentence.replace("\"", "")
    flashcard.sentence_translation = flashcard.sentence_translation.replace("\\n", "\n")
    flashcard.sentence_translation = flashcard.sentence_translation.replace("\"", "")
    return flashcard

CARD_WIDTH_DIV = 2
CARD_HEIGHT_DIV = 6
MARGIN = 10
TEXT_MARGIN = 15
FRONT_MARGIN = 23
PHONETIC_MARGIN = 34
TRANSLATION_MARGIN = 55
SENTENCE_MARGIN = 73
SENTENCE_TRANSLATION_MARGIN = 89
MIN_TRIGGER_MARGIN = 97

def write_card_text(c, x, y, card_height, text, font, size, margin):
    textobject = c.beginText()
    textobject.setTextOrigin(x + TEXT_MARGIN, y + card_height - margin)
    textobject.setFont(font, size)
    textobject.textLines(text)
    c.drawText(textobject)

def wrap_text_and_adjust_margin(text, max_width, font_size):
    lines = textwrap.wrap(text, max_width)
    # Adjust margin increment based on font size.
    margin_increment = font_size / 2
    return '\n'.join(lines), len(lines) * margin_increment

def create_flashcards_pdf(flashcards, filename, strn_max_width):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    card_width = width / CARD_WIDTH_DIV
    card_height = height / CARD_HEIGHT_DIV

    for i, flashcard in enumerate(flashcards):
        flashcard = replace_special_characters(flashcard)
        x = (i % 2) * card_width
        y = height - ((i // 2) % CARD_HEIGHT_DIV) * card_height - card_height
        if i != 0 and i % 12 == 0:
            c.showPage()
            y = height - card_height
        c.rect(x + MARGIN, y + MARGIN, card_width - 2 * MARGIN, card_height - 2 * MARGIN)

        phonetic_margin = PHONETIC_MARGIN
        translation_margin = TRANSLATION_MARGIN
        sentence_margin = SENTENCE_MARGIN
        sentence_translation_margin = SENTENCE_TRANSLATION_MARGIN

        front_font_size = 13
        phonetic_font_size = 8
        translation_font_size = 12
        sentence_font_size = 10
        sentence_translation = 10

        # Wrap long lines of text and adjust margins accordingly
        flashcard.front, front_margin_increase = wrap_text_and_adjust_margin(flashcard.front, strn_max_width-15, front_font_size)
        flashcard.phonetic, phonetic_margin_increase = wrap_text_and_adjust_margin(flashcard.phonetic, strn_max_width*2, phonetic_font_size)
        flashcard.translation, translation_margin_increase = wrap_text_and_adjust_margin(flashcard.translation, strn_max_width-7, translation_font_size)
        flashcard.sentence, sentence_margin_increase = wrap_text_and_adjust_margin(flashcard.sentence, strn_max_width+8, sentence_font_size -1 if sentence_translation_margin >= MIN_TRIGGER_MARGIN else sentence_font_size)
        flashcard.sentence_translation, sentence_translation_margin_increase = wrap_text_and_adjust_margin(flashcard.sentence_translation, strn_max_width+7, sentence_translation -1 if sentence_translation_margin >= MIN_TRIGGER_MARGIN else sentence_translation)

        phonetic_margin += front_margin_increase
        translation_margin += phonetic_margin_increase
        sentence_margin += translation_margin_increase
        sentence_translation_margin += sentence_margin_increase + 5

        # Write text on card
        write_card_text(c, x, y, card_height, flashcard.front, "Helvetica-Bold", front_font_size, FRONT_MARGIN)
        write_card_text(c, x, y, card_height, flashcard.phonetic, "Helvetica", phonetic_font_size, phonetic_margin)
        write_card_text(c, x, y, card_height, flashcard.translation, "Helvetica-Oblique", translation_font_size, translation_margin)
        write_card_text(c, x, y, card_height, flashcard.sentence, "Helvetica", sentence_font_size -1 if sentence_translation_margin >= MIN_TRIGGER_MARGIN else sentence_font_size, sentence_margin)
        write_card_text(c, x, y, card_height, flashcard.sentence_translation, "Helvetica-Oblique", sentence_translation -1 if sentence_translation_margin >= MIN_TRIGGER_MARGIN else sentence_translation, sentence_translation_margin)

    c.showPage()
    c.save()


def main():
    root_path = "D:\\Path_To_CSV\\FlashCards\\"
    flashcards = read_flashcards_from_csv(root_path + "flashcards_nl_in.csv")
    create_flashcards_pdf(flashcards, root_path + "flashcards.pdf", max_width)

if __name__ == "__main__":
    main()
