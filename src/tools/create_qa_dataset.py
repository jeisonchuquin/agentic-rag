import pandas as pd
from ..config import opik_client, QA_DATABASE_1, QA_DATABASE_2

# BASE 1
test_dataset = pd.read_excel(QA_DATABASE_1)
test_dataset['Question'] = test_dataset['Question'].str.strip()
test_dataset['Answer'] = test_dataset['Answer'].str.strip()

input_keys = ["Question"]
output_keys = ["Answer"]

# creamos el dataset de test en opik
dataset = opik_client.get_or_create_dataset(
    name="preguntasyrespuestas_clean",
    description='Dataset con preguntas y respuestas generadas por estudiantes de la USFQ'
)
dataset.insert_from_pandas(
    test_dataset,
    keys_mapping={'Question': input_keys[0], 'Answer': output_keys[0]},
)


# BASE 2
test_dataset = pd.read_excel(QA_DATABASE_2)
test_dataset['Question'] = test_dataset['Question'].str.strip()
test_dataset['Answer'] = test_dataset['Answer'].str.strip()

input_keys = ["Question"]
output_keys = ["Answer"]

# creamos el dataset de test en opik
dataset = opik_client.get_or_create_dataset(
    name="usfq-qa-dataset-v2",
    description='Dataset con preguntas y respuestas generadas por chatgpt'
)
dataset.insert_from_pandas(
    test_dataset,
    keys_mapping={'Question': input_keys[0], 'Answer': output_keys[0]},
)
