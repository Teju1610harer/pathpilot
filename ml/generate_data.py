import random
import pandas as pd

random.seed(42)

CAREERS = [
    "Engineering & Technology", "Healthcare & Medicine", "Business & Finance",
    "Law", "Teaching & Education", "Design & Creative Arts",
    "Government & Defense Services", "Skilled Trades",
    "IT & Computer Applications", "Hospitality & Culinary",
    "Agriculture & Allied Sciences", "Psychology & Social Work"
]

PROFILES = {
    "Engineering & Technology":      (4, 5, 2, 2, 3, 3, 1, 1, 0, 1),
    "Healthcare & Medicine":         (2, 5, 2, 5, 2, 3, 1, 1, 1, 0),
    "Business & Finance":            (2, 3, 2, 3, 5, 4, 1, 1, 1, 0),
    "Law":                           (1, 3, 2, 4, 4, 3, 1, 0, 1, 0),
    "Teaching & Education":          (2, 3, 3, 5, 3, 3, 0, 0, 1, 0),
    "Design & Creative Arts":        (2, 2, 5, 3, 3, 2, 0, 0, 1, 1),
    "Government & Defense Services": (4, 2, 1, 4, 4, 4, 0, 0, 0, 1),
    "Skilled Trades":                (5, 2, 2, 2, 2, 3, 0, 0, 0, 1),
    "IT & Computer Applications":    (3, 5, 2, 2, 3, 3, 1, 1, 0, 1),
    "Hospitality & Culinary":        (3, 2, 4, 4, 4, 2, 0, 0, 1, 0),
    "Agriculture & Allied Sciences": (4, 3, 2, 3, 3, 3, 0, 1, 0, 0),
    "Psychology & Social Work":      (2, 4, 3, 5, 2, 2, 0, 0, 1, 0),
}

FEATURE_NAMES = ["realistic", "investigative", "artistic", "social", "enterprising",
                  "conventional", "logical", "numerical", "verbal", "spatial"]

def add_noise_likert(value, spread=1):
    noisy = value + random.randint(-spread, spread)
    return max(1, min(5, noisy))

def add_noise_binary(value):
    if random.random() < 0.2:
        return 1 - value
    return value

rows = []
SAMPLES_PER_CAREER = 40

for career, profile in PROFILES.items():
    for _ in range(SAMPLES_PER_CAREER):
        row = {}
        for i, feature in enumerate(FEATURE_NAMES):
            base_value = profile[i]
            if feature in ["logical", "numerical", "verbal", "spatial"]:
                row[feature] = add_noise_binary(base_value)
            else:
                row[feature] = add_noise_likert(base_value)
        row["class"] = random.choice(["10th", "12th"])
        row["career"] = career
        rows.append(row)

df = pd.DataFrame(rows)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("data/students.csv", index=False)

print(f"Generated {len(df)} rows across {len(PROFILES)} careers.")
print(df.head())