# 🚀 Code Buddy - AI-Powered Code Profiler

### Authors: Caleb Peters, Matt Simone, Alex Mulder
### Institution: Grand Valley State University
### Course: CIS 350

## 1. Abstract
An intelligent Python source code analysis tool built with Streamlit and powered by Groq (Llama 3.3). This application provides automated Big-O complexity analysis, security flaw detection, code refactoring, and documentation generation.

## 2. Introduction
* **Big-O Analysis**: Determines Time and Space complexity with detailed explanations.
* **Static Analysis**: Identifies performance bottlenecks, security concerns, and PEP 8 violations.
* **Automated Refactoring**: Generates a clean version of your code with type hints, docstrings, and improved readability.
* **README Generation**: Automatically creates a technical README.md for the analyzed code.
* **Downloadable Reports**: Export your refactored code and documentation instantly as .py and .md files.
* **Security-First**: Uses strict system prompts to treat input code as data only and validates syntax via ast.

## 3. Architectural Design
### 🛠️ Tech Stack
* **Frontend**: Streamlit
* **LLM**: Groq Cloud (Model: llama-3.3-70b-versatile)
* **Language**: Python 3.x
* **Environment Management**: python-dotenv
### 📁 Project Structure
* **app.py**: The Streamlit frontend, UI components, and input validation logic.
* **analyzer.py**: The backend engine containing LLM prompts, Groq client integration, and JSON response validation.
* **.env**: Environment configuration for API keys.
### 3.1 Class Diagram
### 3.2 Use Case Diagram
### 3.3 Sequence Diagram

## 4. User Guide/Implementation
### Prerequisites
* A Groq API Key (Get one at console.groq.com)
* Python 3.8 or higher

### Installation & Usage
1. Clone the repository: 
    ```git clone https://github.com/Arcerite/CAM_CODING_PROFILER```
2. Install dependencies: 
    ```bash
    pip install -r requirements.txt
    ```

3. Configure Environment: Create a .env file and add
    ``` GROQ_API_KEY=your_key_here```
4. Run the App: 
    ```python 
    python -m streamlit run app.py
    ```

## 5. Risk Analysis and Retrospective
### 🔒 Security & Validation
* **AST Parsing**: Before processing, input code is parsed via Python's ast module to ensure it is syntactically valid.
* **JSON Schema Validation**: Includes a robust validation function to ensure the AI's response adheres to the required big_o, flaws, and suggestions keys.
* **Input Sanitization**: Limits on input size (15,000 characters) to prevent excessive API usage or overhead.

## 6. Future Scope

## 7. Conclusion

## 8. Walkthrough

## 📝 License
Distributed under the MIT License.
