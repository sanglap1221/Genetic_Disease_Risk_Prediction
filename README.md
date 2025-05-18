# 🧬 Genetic Disease Risk Prediction
Developed a Machine Learning-powered Streamlit web application that predicts the risk of genetic diseases in offspring based on family history and genetic traits.

🔍 Key Features:

Predicts the likelihood of a child inheriting a genetic disease using a trained ML model (Random Forest).

User-friendly Streamlit UI allows users to:

Select or input family history (parents, grandparents).

Choose or input gender of the baby (or mark it unknown).

View risk level (Low / Moderate / High) & percentage based on the model’s prediction.

Displays relevant disease symptoms and inheritance patterns (e.g., autosomal dominant/recessive, X-linked, mitochondrial).

Suggests basic preventive care or treatment options based on the risk.

🧠 Backend:

Trained on a custom dataset with features related to inheritance types and symptoms.

Exported the trained model as .pkl and used it in app.py to make real-time predictions.

🧪 Tech Stack:

Python, Scikit-learn, Pandas, Streamlit

Pickled model and features used for prediction and form generation

This tool is designed as a helpful aid for genetic counselors, clinicians, or concerned parents to assess potential genetic risks early, enabling proactive healthcare planning.

# To run it :
We have to run the code:-- "streamlit run app.py"

![Screenshot from 2025-05-18 12-08-32](https://github.com/user-attachments/assets/d82165b9-0bdb-461c-b6fc-befe9d81597e)
![Screenshot from 2025-05-18 12-08-28](https://github.com/user-attachments/assets/88bdb2c4-62c8-43a9-a761-ce8d44f5b3bc)
