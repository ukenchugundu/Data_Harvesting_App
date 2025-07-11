# Data_Harvesting_App
A Streamlit web app to fetch YouTube channel videos, view statistics, and check subscription status using the YouTube Data API
# YouTube Channel Data Analyzer (Streamlit App)

**A Streamlit web app to fetch YouTube channel videos, view statistics, and check public subscription status using the YouTube Data API.**

![Streamlit App Screenshot - Placeholder](https://via.placeholder.com/800x400?text=Your+Streamlit+App+Screenshot+Here)
*Replace this with an actual screenshot of your running app.*

# Table of Contents

- [About The Project](#about-the-project)
- [Features](#features)
- [Live Demo](#live-demo)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [API Key Setup](#api-key-setup)
  - [Installation](#installation)
  - [Running Locally](#running-locally)
- [Deployment on Streamlit Community Cloud](#deployment-on-streamlit-community-cloud)
- [Understanding API Key and Private Subscriptions](#understanding-api-key-and-private-subscriptions)
- [Built With](#built-with)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

## About The Project

This Streamlit application provides an interactive and user-friendly interface to explore public data from any YouTube channel. Leveraging the Google YouTube Data API v3, it allows users to:

* Retrieve and display recent videos from a specified channel's uploads playlist.
* View key channel statistics such as total subscriber count and the number of public channels it is subscribed to.
* Perform a specific check to see if the main input channel is publicly subscribed to another target channel.

This tool is useful for content creators, researchers, or anyone interested in gaining quick insights into YouTube channel content and basic analytics.

## Features

* **Channel Video Fetching:** Retrieve a list of recent videos (titles, descriptions, thumbnails, publish dates) from any valid YouTube Channel ID.
* **Comprehensive Channel Statistics:** Displays the total subscriber count for the input channel.
* **Public Subscriptions Count:** Shows the number of channels the input channel is publicly subscribed to.
* **Targeted Subscription Check:** Allows you to input a second channel ID and check if the main channel is publicly subscribed to it.
* **Video Details:** Includes video likes and direct links to watch on YouTube.
* **Search & Filter:** Search functionality to filter videos by title.
* **Flexible Display:** Toggle between full video cards with details or a compact list of just video titles.
* **Load More:** Efficiently load additional video cards in batches.
* **Responsive UI:** Designed with Streamlit's intuitive interface for a smooth user experience.

## Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-streamlit-app-url.streamlit.app/)
*Replace `https://your-streamlit-app-url.streamlit.app/` with the actual URL after deployment.*

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Python 3.8+
* `pip` (Python package installer)

### API Key Setup

1.  **Obtain a YouTube Data API v3 Key:**
    * Go to the [Google Cloud Console](https://console.cloud.google.com/).
    * Create a new project or select an existing one.
    * Navigate to "APIs & Services" > "Enabled APIs & Services".
    * Search for and enable "YouTube Data API v3".
    * Go to "APIs & Services" > "Credentials".
    * Click "Create Credentials" > "API Key". Copy your newly generated API key.
    * **Restrict your API Key!** For production, it's highly recommended to restrict your API key to only allow requests from your Streamlit app's domain (if deployed) and/or by API type (YouTube Data API v3).

2.  **Create `secrets.toml`:**
    * In the root directory of your project (where `youtube_app.py` is), create a folder named `.streamlit`.
    * Inside the `.streamlit` folder, create a file named `secrets.toml`.
    * Add your API key to this file like so:
        ```toml
        API_KEY="YOUR_ACTUAL_YOUTUBE_API_KEY_HERE"
        ```
    * **IMPORTANT:** Add `.streamlit/secrets.toml` to your `.gitignore` file to prevent accidentally committing your API key to your public repository.

### Installation

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
    cd YOUR_REPOSITORY_NAME
    ```
    (Replace `YOUR_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual GitHub details.)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    * On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    The `requirements.txt` file should look like this:
    ```
    streamlit
    google-api-python-client
    pandas
    ```

### Running Locally

After completing the setup:

```bash
streamlit run youtube_app.py
