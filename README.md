# 🚀 AI-Powered Code Profiler

An intelligent Python source code analysis tool built with Streamlit and powered by Groq (Llama 3.3). This application provides automated Big-O complexity analysis, security flaw detection, code refactoring, and documentation generation.

## ✨ Features

* **Big-O Analysis**: Determines Time and Space complexity with detailed explanations.
* **Static Analysis**: Identifies performance bottlenecks, security concerns, and PEP 8 violations.
* **Automated Refactoring**: Generates a clean version of your code with type hints, docstrings, and improved readability.
* **README Generation**: Automatically creates a technical README.md for the analyzed code.
* **Downloadable Reports**: Export your refactored code and documentation instantly as .py and .md files.
* **Security-First**: Uses strict system prompts to treat input code as data only and validates syntax via ast.

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **LLM**: Groq Cloud (Model: llama-3.3-70b-versatile)
* **Language**: Python 3.x
* **Environment Management**: python-dotenv

## 🚀 Getting Started

### Prerequisites
* A Groq API Key (Get one at console.groq.com)
* Python 3.8 or higher

### Installation & Usage
1. Clone the repository: 
    ```git clone https://github.com/your-username/ai-code-profiler.git```
2. Install dependencies: 
    ```bash
    pip install streamlit groq python-dotenv
    ```

3. Configure Environment: Create a .env file and add
    ``` GROQ_API_KEY=your_key_here```
4. Run the App: 
    ```python 
    streamlit run app.py
    ```

## 📁 Project Structure

* **app.py**: The Streamlit frontend, UI components, and input validation logic.
* **analyzer.py**: The backend engine containing LLM prompts, Groq client integration, and JSON response validation.
* **.env**: Environment configuration for API keys.

## 🔒 Security & Validation

* **AST Parsing**: Before processing, input code is parsed via Python's ast module to ensure it is syntactically valid.
* **JSON Schema Validation**: Includes a robust validation function to ensure the AI's response adheres to the required big_o, flaws, and suggestions keys.
* **Input Sanitization**: Limits on input size (15,000 characters) to prevent excessive API usage or overhead.

## 📝 License
Distributed under the MIT License.
