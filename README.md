# 📰 News and Sentiment Analyzer 🗞️

## Table of Contents

* [Introduction](#introduction)
* [Features](#features)
* [How It Works](#how-it-works)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Local Setup](#local-setup)
    * [AWS Deployment](#aws-deployment)
* [Project Structure](#project-structure)
* [API Key](#api-key)
* [Future Enhancements](#future-enhancements)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

---

## Introduction

Welcome to the **News and Sentiment Analyzer**! This interactive Streamlit application provides a powerful platform to explore global news with insightful sentiment analysis and topic clustering. Designed for curious minds, researchers, and anyone interested in understanding public sentiment, this tool goes beyond just fetching headlines.

It empowers users to:
* **Search for News:** Effortlessly find articles from various countries and categories, or drill down with specific keywords.
* **Uncover Sentiment:** Get an immediate understanding of the **emotional tone** (positive, negative, or neutral) behind news articles.
* **Discover Hidden Patterns:** Utilize advanced clustering to group similar news articles, revealing underlying themes and connections.
* **Generate Comprehensive Reports:** Access yearly news reports that visualize sentiment trends, top categories, and frequent keywords.

---

## Features

This application offers a rich set of functionalities:

* **Flexible News Search:**
    * Filter news by **country**, **category** (Business, Entertainment, Health, Science, Sports, Technology, Headlines), or by **custom keywords**.
    * Specify a date range for your news search.
* **Detailed Sentiment Breakdown:**
    * For each article, view scores for **negative, neutral, positive, and compound sentiment**, along with an **overall sentiment classification**.
* **Dynamic News Clustering:**
    * Visualize prominent topics and themes across a historical news dataset using **Word Clouds** for each cluster.
    * Input a custom query and instantly see which news cluster it belongs to, along with its sentiment analysis.
* **Annual Reporting:**
    * Generate insightful reports for selected years, featuring:
        * 📊 **Overall Sentiment Distribution Pie Chart**
        * 📈 **Monthly Sentiment Trend Line Chart**
        * 🏆 **Top Categories by Volume Bar Chart**
        * 📝 **Most Frequent Keywords Word Cloud**
        * 🌈 **Average Sentiment by Category Bar Chart**

---

## How It Works

The News and Sentiment Analyzer leverages a robust stack of technologies:

* **Frontend:** Built with **Streamlit** for a dynamic and interactive user interface.
* **News Data:** Integrates with the **GNews API** to fetch real-time and historical news articles from a vast array of sources.
* **Natural Language Processing (NLP):**
    * Employs **NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner)** for nuanced sentiment analysis, processing text to determine its emotional charge.
    * Includes custom text preprocessing (lowercase, removal of non-alphabetic characters, stop word removal) to clean text for analysis.
* **Machine Learning for Clustering:**
    * Utilizes **TF-IDF Vectorization** to convert text content into numerical features.
    * Applies **K-Means Clustering** to group news articles based on their textual similarity, identifying key topics and narratives.
* **Data Handling:** Uses **Pandas** for efficient data manipulation and analysis.
* **Visualization:** Presents complex data in an easy-to-understand format using **Matplotlib** and **WordCloud**.
* **Deployment (AWS):** The application is designed for deployment on **Amazon Web Services (AWS)**, leveraging:
    * **Amazon S3:** For storing static assets, specifically your historical news data CSVs (`combined.csv`, `combinedsent.csv`).
    * **Amazon RDS:** For a robust and scalable database solution to store processed news data.
    * **AWS compute services (e.g., EC2, Elastic Beanstalk):** To host and run the Streamlit application.

---

## Getting Started

Follow these steps to get a copy of the project up and running on your local machine for development and testing, or understand its conceptual AWS deployment.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.8+**
* **pip** (Python package installer)
* **Git** (for cloning the repository)
* A **GNews API key** (You can get one from [https://gnews.io/](https://gnews.io/)).

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Jeyavani2/NewsSentiment.git](https://github.com/Jeyavani2/NewsSentiment.git)
    cd NewsSentiment
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required Python packages:**
    Create a `requirements.txt` file in the root of your `NewsSentiment` directory with the following content:
    ```
    streamlit
    requests
    pandas
    scikit-learn
    matplotlib
    wordcloud
    nltk
    ```
    Then, install them:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLTK resources:**
    The application attempts to download `stopwords` and `vader_lexicon` if not found. You can also manually download them:
    ```python
    import nltk
    nltk.download('stopwords')
    nltk.download('vader_lexicon')
    ```

5.  **Place your GNews API Key:**
    The current code hardcodes the API key. For local testing, you can modify the `API_KEY` variable in `NewsStream.py` with your obtained key. For production, consider using environment variables.

6.  **Prepare Data Files (for Cluster and Report features):**
    The `Cluster` and `Report` sections rely on `combined.csv` and `combinedsent.csv`.
    * **Create these CSV files:** These files should contain historical news data with columns like `headline`, `short_description`, `date`, and `category`. `combinedsent.csv` should additionally contain sentiment-related columns (`Negative`, `Positive`, `Neutral`, `Compound`, `Overall_sentiment`).
    * **Adjust paths:** In `NewsStream.py`, change the hardcoded paths `r'c:\users\91904\combined.csv'` and `r'c:\users\91904\combinedsent.csv'` to relative paths within your project (e.g., `data/combined.csv`) and ensure the files are placed there.

7.  **Run the Streamlit application:**
    ```bash
    streamlit run NewsStream.py
    ```
    This will open the application in your web browser.

### AWS Deployment

This project is designed for deployment on Amazon Web Services (AWS) using:

* **Amazon S3:** Used as a scalable storage solution for historical news data files (`combined.csv`, `combinedsent.csv`). Your Streamlit application will read these files directly from S3.
* **Amazon RDS:** A managed relational database service (e.g., PostgreSQL, MySQL) to store and manage structured news data for more robust and scalable data operations.
* **AWS Compute (e.g., EC2, Elastic Beanstalk, ECS):** To host the Streamlit application.
    * **EC2:** For manual setup and fine-grained control over the server environment.
    * **Elastic Beanstalk:** A higher-level service that automates the deployment, scaling, and management of web applications. This is often a good choice for Streamlit apps.
    * **ECS (Elastic Container Service):** For containerizing the application using Docker and running it on a scalable container orchestration platform.

**Deployment Steps (Conceptual):**

1.  **Configure AWS Credentials:** Ensure your AWS CLI and SDKs are configured with appropriate IAM user or role credentials.
2.  **Upload Data to S3:** Upload `combined.csv` and `combinedsent.csv` to your designated S3 bucket. Modify your `NewsStream.py` to read from S3 using `boto3`.
3.  **Set up RDS:** Create an RDS instance and, if applicable, migrate your data into database tables. Update `NewsStream.py` to connect to and query the RDS database.
4.  **Deploy Streamlit App:**
    * **For Elastic Beanstalk:** Create a new application, choose the Python environment, upload your project folder (including `NewsStream.py`, `requirements.txt`, and any data files if not using S3/RDS for all), and let Elastic Beanstalk handle the deployment.
    * **For EC2/ECS:** Set up your EC2 instance or ECS cluster, install dependencies, and run your Streamlit application, potentially behind a web server (like Nginx) for production access.
5.  **Configure Security:** Set up appropriate AWS VPC, Security Groups, and IAM roles to control access and ensure secure communication between your application, S3, and RDS.




## API Key

This project uses the GNews API. Please obtain your API key from [https://gnews.io/](https://gnews.io/). For security, it is highly recommended to store your API key as an environment variable rather than hardcoding it directly in the script, especially in a deployed environment.



## Future Enhancements

* **Dynamic Data Ingestion:** Implement a script or AWS Lambda function to regularly fetch new news data from the GNews API and update the S3 files or RDS database automatically.
* **Improved API Key Management:** Fully transition to environment variables or AWS Secrets Manager for all API keys and sensitive credentials.
* **Advanced NLP Models:** Explore using more sophisticated pre-trained NLP models (e.g., from Hugging Face Transformers) for potentially higher accuracy in sentiment analysis or more detailed topic modeling.
* **User Interface Refinements:** Enhance the Streamlit UI with more interactive elements, filtering options, and potentially user accounts.
* **Robust Error Handling:** Implement more comprehensive error handling and logging, especially for API calls and data processing.

