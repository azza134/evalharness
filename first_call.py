import anthropic
from dotenv import load_dotenv

load_dotenv()  

client = anthropic.Anthropic()
passage = open("permit.txt").read()

# Question that tests if the model can get a question right that has the answer disclosed in the passage.
in_doc_question = "What are the requirements for the toilet facilities?"

# Question whose answer is NOT in the passage. If the model provides an answer that includes information outside of the passage it proves that the model is not 100% faithful.

out_of_doc_question = "What is the minimum ceiling height for a habitable room in NSW?"

# Three levels of how hard the instruction points the model at the passage. The passage itself is ALWAYS supplied in the user message (see ask() below) -- the levels only change the instruction about it. 
# STRONG forces exclusive use of the passage, MODERATE mentions a passage is available, WEAK gives no instruction about whether to rely on it or restrict itself to it.
STRONG = (
    "Answer using ONLY the passage. If the passage does not contain the answer, "
    "reply exactly: NOT IN DOCUMENT. Never use outside knowledge."
)
MODERATE = "Answer the question. Here is a passage that may help."
WEAK = "Answer the question."


def ask(system_instruction, question, doc):
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=400,
        system=system_instruction,
        messages=[{
            "role": "user",
            "content": "Passage:\n" + doc + "\n\nQuestion: " + question,
        }],
    )
    return "".join(b.text for b in response.content if b.type == "text")


print("=== WHEN THE ANSWER TO QUESTION IS IN PASSAGE ===")
print("STRONG →")
print(ask(STRONG, in_doc_question, passage))
print("\nMODERATE →")
print(ask(MODERATE, in_doc_question, passage))
print("\nWEAK →")
print(ask(WEAK, in_doc_question, passage))

print("\n\n=== WHEN THE ANSWER TO QUESTION IS NOT IN PASSAGE ===")
print("STRONG →")
print(ask(STRONG, out_of_doc_question, passage))
print("\nMODERATE →")
print(ask(MODERATE, out_of_doc_question, passage))
print("\nWEAK →")
print(ask(WEAK, out_of_doc_question, passage))


# Perturbation test: Replace 20 with 13 to see if the model will follow this change to see if the model actually read the passage.

perturbed_passage = (
    passage
    .replace("every 20", "every 13")
    .replace("part of 20 persons", "part of 13 persons")
)
# Assertion confirms that the replacements actually took place, or output would deceive users into thinking the changes were made when they weren't, skewing evaluation.
assert perturbed_passage != passage, "replace() changed nothing -- target text isn't an exact match in permit.txt. Fix before trusting the result."

# Probe question targets the one fact we change, so the answer is just the number (easy to read/score).
probe_question = "How many persons per toilet are required on the work site?"

print("\n\n=== PERTURBATION TEST ===")
print("Question:", probe_question)
print("Perturbed passage replaced every instance of 20 with 13")

levels = [("STRONG", STRONG), ("MODERATE", MODERATE), ("WEAK", WEAK)]

for name, instruction in levels:
    baseline = ask(instruction, probe_question, passage)             # doc says 20
    perturbed = ask(instruction, probe_question, perturbed_passage)  # doc says 13
    print(name, "→")
    print("  ORIGINAL  (doc=20): ", " ".join(baseline.split()))
    print("  PERTURBED (doc=13): ", " ".join(perturbed.split()))
    print()

print("-> follows to 13 = the answer is sensitive to the document's stated value.")
print("   stays at 20 = prior knowledge may be relying on prior knowledge or failing to acknowledge the adjusted passage.")
