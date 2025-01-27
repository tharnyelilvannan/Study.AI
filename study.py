from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
import run

client = OpenAI()

def create_assistant():
    assistant = client.beta.assistants.create(
        name="Study.AI",
        instructions=(
            "Create a detailed set of questions and answers based on the content of a student's notes from a PDF file. "
            "The goal is to aid the student in studying and testing their knowledge effectively.\n\n"
            "Steps:\n"
            "1. **Extract Content:** Extract and read the text content from the PDF file containing the student's notes.\n"
            "2. **Identify Key Topics:** Identify the main topics, headings, and subheadings present in the notes to understand the major themes.\n"
            "3. **Generate Questions:** For each key topic, craft questions that cover definitions, explanations, and critical concepts. "
            "Include a mix of question types such as multiple-choice, short answer, and true/false for variety.\n"
            "4. **Provide Answers:** Develop clear and concise answers or explanations to the questions generated. "
            "Ensure that answers are accurate and align with the content of the notes.\n"
            "5. **Organize:** Ensure the questions and answers are organized by topic for easy study reference.\n"
            "6. **Put Content into CSV File:** Place all questions and answers into a CSV file. Ensure it is organized and easily readable.\n\n"
            "Output Format:\n"
            "The output should be structured as a list of questions followed by their corresponding answer as a CSV. "
            "Each question should be followed immediately by its answer.\n\n"
            "Example format:\n"
            "[Question], [Answer]\n"
            "Examples:\n"
            "**Example Input:**\n"
            "- Notes Topic: Photosynthesis Process\n"
            "- Content Excerpt: [Photosynthesis is the process by which green plants and some other organisms use sunlight "
            "to synthesize nutrients from carbon dioxide and water. The process involves chlorophyll and generates oxygen as a byproduct.]\n\n"
            "**Example Output:**\n"
            "- **Topic: Photosynthesis Process**\n"
            "What is photosynthesis?, Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize nutrients from carbon dioxide and water, generating oxygen as a byproduct.\n"
            "What is the role of chlorophyll in photosynthesis, Chlorophyll absorbs sunlight, providing the energy needed to drive the process of photosynthesis.\n\n"
            "(Real examples should cover the entirety of the provided notes, generating a proportional number of questions and answers.)\n\n"
            "Notes:\n"
            "- Ensure that questions address all significant concepts within the provided notes.\n"
            "- Consider varying the difficulty of questions to accommodate a range of student proficiency levels.\n"
            "- When dealing with complex PDFs, ensure that the extraction process maintains context and coherence for accurate question generation."
            "- Put all the questions and answers into a TXT file. The format should be: Question, Answer. They should be separated with a comma."
        ),
        tools=[{"type": "file_search"}],
        model="gpt-4o",
    )
    return assistant

def generate_questions(text):

    assistant = create_assistant()

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )
    with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user formally.",
    event_handler=EventHandler(),
    ) as stream:
        stream.until_done()