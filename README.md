## **Flashcard PDF Generator**

Flashcard PDF Generator is a Python application that helps users create printable flashcards from a CSV file. The application reads from a CSV file, generates a PDF with flashcards, and each card contains front text, phonetic transcription, translation, sentence, and sentence translation.

The flashcards are useful for learning a new language, studying for an exam, or memorizing any type of data.

### **Features**
-	Generates a PDF from a CSV file
-	Customizable text position based on text length
-	Supports long sentences and wraps text accordingly
-	Unicode support

#### **Installation**

You need Python 3.6 or later to run Flashcard PDF Generator. You can check your Python version by running:

	python --version

You will also need the following Python packages:

	csv
	reportlab
	textwrap

You can install them with pip:

	pip install reportlab

(No need to install csv and textwrap, as they are part of the Python Standard Library.)


#### **Usage**

Prepare your flashcard data in a CSV file. The format should be: front, phonetic, translation, sentence, sentence_translation. See flashcards_nl_in.csv for an example.
Change the file-path of the variable called root_path


Run the script:

python flashcards.py


##### **Contributing**

Contributions are welcome! Please contact me if you have any contributions.

##### **License**
This project is licensed under the terms of the MIT license.
If you use this code, a mention would be apreciated.
