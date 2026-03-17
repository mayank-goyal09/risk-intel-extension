import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import re

# ============================================================
# PHASE 1: Text Cleaning (No spaCy needed - keeps things light)
# ============================================================
def clean_text(text):
    """Professional text cleaning without heavy NLP libraries."""
    text = text.lower().strip()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep meaningful punctuation
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

# ============================================================
# PHASE 2: Load and Prepare Data
# ============================================================
print("📂 Loading training data...")
df = pd.read_csv('tos_data.csv')
df['cleaned'] = df['text'].apply(clean_text)

print(f"   Total samples: {len(df)}")
print(f"   Predatory (1): {sum(df['label'] == 1)}")
print(f"   Safe (0):      {sum(df['label'] == 0)}")
print(f"   Balance ratio: {sum(df['label'] == 1) / len(df):.1%} predatory")

# ============================================================
# PHASE 3: Build a High-Precision Pipeline
# ============================================================
print("\n🏗️  Building pipeline...")

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 3),       # Unigrams, bigrams, AND trigrams for better context
        max_features=3000,        # Keep model size small
        min_df=1,                 # Include even rare terms (small dataset)
        max_df=0.95,              # Exclude terms in >95% of docs (too common)
        sublinear_tf=True,        # Apply log normalization to TF (reduces impact of frequency)
    )),
    ('clf', RandomForestClassifier(
        n_estimators=200,         # More trees = more stable predictions
        max_depth=15,             # Prevent overfitting
        min_samples_leaf=2,       # Each leaf needs at least 2 samples
        class_weight='balanced',  # Handle any class imbalance
        random_state=42,          # Reproducible results
        n_jobs=-1                 # Use all CPU cores
    ))
])

# ============================================================
# PHASE 4: Cross-Validation (Honest Evaluation)
# ============================================================
print("\n📊 Running 5-Fold Cross Validation...")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Accuracy
acc_scores = cross_val_score(pipeline, df['cleaned'], df['label'], cv=cv, scoring='accuracy')
print(f"   Accuracy:  {acc_scores.mean():.1%} (+/- {acc_scores.std():.1%})")

# Precision (what we care about most - don't flag safe clauses as predatory!)
prec_scores = cross_val_score(pipeline, df['cleaned'], df['label'], cv=cv, scoring='precision')
print(f"   Precision: {prec_scores.mean():.1%} (+/- {prec_scores.std():.1%})")

# Recall (don't miss actual predatory clauses)
rec_scores = cross_val_score(pipeline, df['cleaned'], df['label'], cv=cv, scoring='recall')
print(f"   Recall:    {rec_scores.mean():.1%} (+/- {rec_scores.std():.1%})")

# F1 Score (balance of precision and recall)
f1_scores = cross_val_score(pipeline, df['cleaned'], df['label'], cv=cv, scoring='f1')
print(f"   F1 Score:  {f1_scores.mean():.1%} (+/- {f1_scores.std():.1%})")

# ============================================================
# PHASE 5: Train Final Model on ALL Data
# ============================================================
print("\n🧠 Training final model on all data...")
pipeline.fit(df['cleaned'], df['label'])

# Full classification report on training data (for reference)
y_pred = pipeline.predict(df['cleaned'])
print("\n📋 Classification Report (on training data):")
print(classification_report(df['label'], y_pred, target_names=['SAFE', 'PREDATORY']))

# ============================================================
# PHASE 6: Verify with Test Sentences
# ============================================================
print("=" * 60)
print("🧪 VERIFICATION TESTS")
print("=" * 60)

test_cases = [
    # Should be PREDATORY
    ("We reserve the right to change fees without notice.", True),
    ("You waive your right to a class action lawsuit.", True),
    ("All disputes must be settled through forced arbitration.", True),
    ("We may terminate your account for any reason.", True),
    ("We may sell your data to third parties.", True),
    
    # Should be SAFE
    ("Your privacy is important to us and we protect it.", False),
    ("Users can cancel their subscription at any time.", False),
    ("We do not track your location data.", False),
    ("You can download all your data at any time.", False),
    ("We offer a full refund within 30 days.", False),
    
    # TRICKY / EDGE CASES (should be SAFE - just normal info)
    ("Welcome to our service.", False),
    ("Thank you for choosing our platform.", False),
    ("Please read the following terms carefully.", False),
    ("Contact us at support@example.com for help.", False),
    
    # REAL-WORLD TOS (should be SAFE — these are from Google-style TOS)
    ("We are constantly developing new technologies and features to improve our services.", False),
    ("As part of continual improvement we sometimes add or remove features and functionalities.", False),
    ("If we make material changes that negatively impact your use we will provide you with reasonable advance notice.", False),
    ("We will also provide you with an opportunity to export your content from your account.", False),
]

passed = 0
total = len(test_cases)

for text, expected_predatory in test_cases:
    cleaned = clean_text(text)
    prediction = pipeline.predict([cleaned])[0]
    proba = pipeline.predict_proba([cleaned])[0]
    confidence = max(proba)
    pred_predatory = prediction == 1
    
    is_flagged = pred_predatory and proba[1] > 0.80
    
    status = "✅" if is_flagged == expected_predatory else "❌"
    if is_flagged == expected_predatory:
        passed += 1
    
    label = "PREDATORY" if is_flagged else "SAFE"
    print(f"  {status} [{label:9s} {proba[1]:.0%}] \"{text[:60]}\"")

print(f"\n🎯 Test Results: {passed}/{total} passed")

# ============================================================
# PHASE 7: Save the Model
# ============================================================
model_path = 'tos_model.pkl'
joblib.dump(pipeline, model_path)

import os
model_size = os.path.getsize(model_path)
print(f"\n💾 Model saved as '{model_path}' ({model_size / 1024:.0f} KB)")
print("✅ DONE! Model is ready for the extension.")