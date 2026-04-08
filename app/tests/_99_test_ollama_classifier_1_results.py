import pandas as pd
import json

file = "C:/Users/Chris/Downloads/diplomat/app/tests/_5_output_ollama_test/_1_classifier_outputs/out_2026-04-07_1775556908.csv"

df = pd.read_csv(file)
print(df)

for i in range(0, len(df)):
    print(i)
    df['LLM Output'][i] = json.loads(df['LLM Output'][i])
    

print(df)