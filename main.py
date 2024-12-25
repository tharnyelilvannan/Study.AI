from PyPDF2 import PdfReader
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
import run
import study

file = input("Type path to PDF file.")
reader = PdfReader(file)
page = reader.pages[0]
text = page.extract_text()
generate_questions(text)