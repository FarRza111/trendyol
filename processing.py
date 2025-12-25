# Supervised Learning Example: Classification
# Using the Iris dataset with Random Forest Classifier

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Load dataset
iris = load_iris()
       # Features
y = iris.target_        # Labels

def do_nothing():
    pass


def part1():
    pass

# 2. Split into training & testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 4. Make predictions
y_pred = model.predict(X_test)

# 5. Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# 6. Predict a new sample
sample = [[5.1, 3.5, 1.4, 0.2]]  # Example Iris measurements
prediction = model.predict(sample)
print("Predicted class:", iris.target_names[prediction][0])



