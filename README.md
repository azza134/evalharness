# Faithfulness Evaluation Harness

## The problem

Enterprises are currently integrating AI across their workflows right now in order to modernise and improve efficiency. However, especially in industries where there are lots of documents involved, there is no margin for error because AI hallucinations can be incredibly costly. These industries include construction, legal, healthcare etc. Thus, AI has to be pressure tested heavily to ensure that all outputs are properly grounded in the documents of these enterprises to minimise costly hallucinations, particularly those that result in the models relying on pretrained data rather than the documents it is grounded in.

## What it measures

The harness currently scores two different independent properties.

1. **Context Sensitivity:** By using a perturbation test where we change a detail in the document, we measure if the model is able to follow the change in the document, verifying that the model is using the document to form its output.

2. **Abstention:** By asking a question that is not answered in the document, if the model is able to answer the question, then the model is using information outside of the document to form its output.

It is possible that a model can pass one of the tests and fail the other. All model outputs are printed which allows users to form their own evaluations of the model's performance in this case.

## What's here

- `harness.py` - This is the evaluation harness. It sets the conditions for testing the two properties and sets the three system prompts that reference the document at varying instruction strengths. It prints the model outputs and uses a lexical scorer as well as the option for an LLM judge to grade the outputs as pass or fail. Finally, it prints a Wilson's interval at 95% confidence to test how reliable the results are based on the amount of tests run (n).

- `judge.py` - This is the script that determines if a model is fit to stand as judge for abstention. It tests abstention by providing a test set of questions with differing domains as well as its proximity to the domain of the document and the varying likelihoods that the answer to the question is in the model's pretraining data. After running `judge.py` for the first time, the user will be prompted to grade the results of the gradee in `judge_gold.json`. After this, `judge.py` should be run again. This time, the judge model will grade the results of the gradee and the script will record the raw agreement rate between the human and the test judge, the Cohen's kappa (to what extent is agreement beyond what chance can explain) and the reason for any disagreements that may occur (`judge_results.json`). Based on these metrics the judge will either be passed or failed by the system, but the user can and should review any disagreements to evaluate whether or not the model is fit to judge `harness.py`.

- `document.txt` - paste in the document that you want to test the model's faithfulness on.

- `test_logic.py` - a list of assertions that verify that the metrics and adjustments used in the repo are working as intended

- `requirements.txt` - list of dependencies

## Setup

Clone the repo and run the following command:

```bash
pip install -r requirements.txt
```

Create a new file called `.env` and paste the following: (replace sk-ant-... with your corresponding API key)

```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

## Run

```bash
python3 harness.py
python3 judge.py
python3 -m unittest test_logic -v
```

## Status / limitations

This is a project aimed at solving the problem described earlier and is currently in an early developmental stage. It is a functional prototype that is able to successfully compute all the results and processes that have been described so far. However, the scope and complexity is limited to just two different model providers (Anthropic and OpenAI) and one grounded document which the models being tested have been able to stay faithful to with ease. While the repo is customisable, it requires the user to be able to interpret the code to avoid crashing the code after making adjustments.
