import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

def train_standard():
    df = pd.read_csv("spam_dataset.csv")
    
    pipeline = make_pipeline(TfidfVectorizer(), MultinomialNB())
    pipeline.fit(df["text"], df["label"])
    
    joblib.dump(pipeline, "spam_model.joblib")
    print("Standard scikit-learn model saved to spam_model.joblib")

if __name__ == "__main__":
    train_standard()
