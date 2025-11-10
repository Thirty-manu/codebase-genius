# Project Submission

## 1. Repository
This project is hosted in a **public Git repository** submitted via the Google Form:  
[Insert your repository link here]

## 2. Running the System
To run the system and generate documentation, follow these steps:

```bash
# 1. Clone the repository
git clone <your-repo-link>
cd <your-repo-folder>

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the FastAPI server
uvicorn main:app --reload

# The API will be available at http://127.0.0.1:8000
# Access documentation at http://127.0.0.1:8000/docs
