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
            "6. **Put Content into TXT File:** Place all questions and answers into a TXT file. Ensure it is organized and easily readable.\n\n"
            "Output Format:\n"
            "The output should be structured as a list of questions followed by their corresponding answers, organized by topic. "
            "Each question should be followed immediately by its answer.\n\n"
            "Example format:\n"
            "- **Topic 1: [Main Topic Name]**\n"
            "  - Question 1: [Question related to Topic 1]\n"
            "      - Answer: [Answer for Question 1]\n"
            "  - Question 2: [Question related to Topic 1]\n"
            "      - Answer: [Answer for Question 2]\n\n"
            "Examples:\n"
            "**Example Input:**\n"
            "- Notes Topic: Photosynthesis Process\n"
            "- Content Excerpt: [Photosynthesis is the process by which green plants and some other organisms use sunlight "
            "to synthesize nutrients from carbon dioxide and water. The process involves chlorophyll and generates oxygen as a byproduct.]\n\n"
            "**Example Output:**\n"
            "- **Topic: Photosynthesis Process**\n"
            "  - Question: What is photosynthesis?\n"
            "      - Answer: Photosynthesis is the process by which green plants and some other organisms use sunlight "
            "to synthesize nutrients from carbon dioxide and water, generating oxygen as a byproduct.\n"
            "  - Question: What is the role of chlorophyll in photosynthesis?\n"
            "      - Answer: Chlorophyll absorbs sunlight, providing the energy needed to drive the process of photosynthesis.\n\n"
            "(Real examples should cover the entirety of the provided notes, generating a proportional number of questions and answers.)\n\n"
            "Notes:\n"
            "- Ensure that questions address all significant concepts within the provided notes.\n"
            "- Consider varying the difficulty of questions to accommodate a range of student proficiency levels.\n"
            "- When dealing with complex PDFs, ensure that the extraction process maintains context and coherence for accurate question generation."
        ),
        tools=[{"type": "file_search"}],
        model="gpt-4o",
    )
    return assistant

assistant = create_assistant

thread = client.beta.threads.create()

prompt = input("Enter message or add PDF file.\n")

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=prompt
)
with client.beta.threads.runs.stream(
thread_id=thread.id,
assistant_id=assistant.id,
instructions="Please address the user formally.",
event_handler=EventHandler(),
) as stream:
    stream.until_done()