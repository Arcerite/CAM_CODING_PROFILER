# Code Buddy :) - AI-Powered Code Profiler

### Authors: Caleb Peters, Matt Simone, Alex Mulder
### Institution: Grand Valley State University
### Course: CIS 350

## 1. Abstract
Software development takes time and effort to do well, but **Code Buddy** aims to ease the task for developers of all skill-levels. **Code Buddy** is a website designed to help programmers create better code. Users simply upload their code and the code will be analyzed by AI to offer suggestions including Big O analysis, identified flaws, docstrings, comments, and coding conventions. Then, the user will be able to download the refactored code and the provided README. **Code Buddy** will not only save time, but it will also save developers from headaches by identifying flaws and possible bottlenecks before they arise.

## 2. Introduction
Large Language Models have changed the way that software is developed, but trying to "vibe code" can easily turn into fighting with the model rather than creating quality software. Even if you code something functional with an LLM, it may be riddled with bugs and security risks. **Code Buddy** aims to use AI to build code faster and better without the headaches.

**Code Buddy** is an intelligent Python source code analysis website built with Streamlit and powered by Groq (Llama 3.3). Once the user uploads their code, Groq will analyze it for time and space complexity, performance bottlenecks, security concerns, and PEP 8 violations. Our website will return the report with detailed explanations, a README file, and a new version of the code with type hints, docstrings, and improved readability. The user will be able to export the refactored code and documentation instantly as .py and .md files.

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
To be added...

### 3.2 Use Case Diagram
![Use Case Diagram](UML/usecase_diagram.png)

### 3.3 Sequence Diagram
![Use Case Diagram](UML/sequence_diagram.png)

## 4. User Guide/Implementation
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

## 5. Risk Analysis and Retrospective
### 🔒 Security & Validation
* **AST Parsing**: Before processing, input code is parsed via Python's ast module to ensure it is syntactically valid.
* **JSON Schema Validation**: Includes a robust validation function to ensure the AI's response adheres to the required big_o, flaws, and suggestions keys.
* **Input Sanitization**: Limits on input size (15,000 characters) to prevent excessive API usage or overhead.

## 6. Future Scope
To be added...

## 7. Conclusion
To be added...

## 8. Walkthrough
To be added...