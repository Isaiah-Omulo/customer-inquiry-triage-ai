
# Customer Inquiry Triage AI Service

A complete solution for the CaaVantagePoint AI Software Developer Assessment. This project uses Google's Gemini LLM to automatically categorize customer support messages, routing them to the correct department.



---

##  Table of Contents

- [ Features](#-features)
- [ Technology Stack](#️-technology-stack)
- [ How to Set Up and Run](#-how-to-set-up-and-run)
  - [Prerequisites](#prerequisites)
  - [Part 1: Backend API Setup](#part-1-backend-api-setup)
  - [Part 2: Frontend UI Setup](#part-2-frontend-ui-setup)
- [ API Endpoint Details](#-api-endpoint-details)
- [ Design Choices & Trade-offs](#-design-choices--trade-offs)


---

## Features

-   **AI-Powered Triage**: Leverages Google Gemini for highly accurate, nuanced message classification.
-   **Structured JSON Output**: The API returns a reliable JSON object with category, justification, and a confidence score.
-   **Scalable Categories**: New inquiry categories can be added with minimal code changes.
-   **Interactive UI**: A clean and user-friendly web interface built with Streamlit for easy demonstration and testing.
-   **Decoupled Architecture**: A separate FastAPI backend and Streamlit frontend for modularity and scalability.

---


## How to Set Up and Run

Follow these instructions to get the application running on your local machine.

### Prerequisites

-   **Python 3.9** or higher.
-   **Git** command-line tools.
-   A **Google API Key** with the Gemini API enabled. You can get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Part 1: Backend API Setup

**Open your first terminal window for these steps.**

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Isaiah-Omulo/customer-inquiry-triage-ai.git
    cd customer-inquiry-triage-ai
    ```

2.  **Navigate to the Backend Directory**
    ```bash
    cd backend
    ```

3.  **Create and Activate a Virtual Environment**
    A virtual environment keeps project dependencies isolated.
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate it
    # On macOS or Linux:
    source venv/bin/activate
    # On Windows:
    # venv\Scripts\activate
    ```
    Your terminal prompt should now be prefixed with `(venv)`.

4.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Your API Key**
    The application needs your Google API key to function.
    -   Create a `.env` file by copying the example: `cp .env.example .env`
    -   Open the new `.env` file and paste your key:
        ```env
        # Inside backend/.env
        GOOGLE_API_KEY="AIzaSy...your...actual...api...key..."
        ```

6.  **Run the Backend Server**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API is now running at `http://127.0.0.1:8000`. **Leave this terminal running.**

### Part 2: Frontend UI Setup

**Open a new terminal window or tab for these steps.**

1.  **Navigate to the Frontend Directory**
    From the project's root folder:
    ```bash
    cd frontend
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Frontend Application**
    ```bash
    streamlit run app.py
    ```
    A new tab will automatically open in your web browser at `http://localhost:8501`. You can now interact with the application.

---

##  API Endpoint Details

The backend provides a single endpoint for message triage.

-   **Endpoint:** `POST /triage`
-   **Description:** Accepts a customer message and returns its category, a justification, and a confidence score.
-   **Request Body (JSON):**
    ```json
    {
      "message": "Hello, I can't log into my account."
    }
    ```
-   **Success Response (JSON):**
    ```json
    {
      "category": "TECHNICAL_SUPPORT",
      "reasoning": "The message mentions an inability to 'log into my account,' which is a common technical problem.",
      "score": 0.99
    }
    ```

---

##  Design Choices & Trade-offs

### Classification Logic: LLM with Structured Output

I chose to use **Google Gemini** with the `instructor` library for the core classification logic.

-   **Why an LLM?** Large Language Models excel at understanding semantic context and user intent, making them far more robust and accurate than brittle keyword or regex-based rules. An LLM can easily differentiate between "I want to cancel my plan" (Account Management) and "How much does it cost to cancel?" (Billing Inquiry).
-   **Why Structured Output?** Relying on an LLM to generate raw text can be unreliable. By using `instructor` to enforce a Pydantic model (`TriageResponse`), we guarantee that the LLM's output is always a valid, well-structured JSON object that matches our API's contract. This eliminates fragile parsing logic and makes the system robust.
-   **Trade-offs:** The main trade-offs are dependency on an external API, which introduces network latency and a per-request cost. However, the superior accuracy and ease of development for this kind of nuanced task justify these trade-offs.

### Backend: FastAPI

FastAPI was selected for its high performance, native `async` support (essential for handling I/O-bound API calls to Gemini), and automatic data validation and documentation via Pydantic, which accelerates development and ensures a well-defined API.

### Frontend: Streamlit

Streamlit was the ideal choice for building a clean, interactive UI quickly. It allows the focus to remain on the AI functionality while still providing a professional-looking demonstration platform. For a full-scale production application with complex UI/UX needs, a framework like React would be more suitable, but at a much higher development cost.

---

