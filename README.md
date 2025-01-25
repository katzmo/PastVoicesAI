# Voices from the Past: AI-Driven Storytelling from the Perspective of Cultural Artifacts  

**Voices from the Past** is an AI-powered application that brings cultural artifacts to life by giving them a voice to tell their own stories. Using AI-generated first-person narratives, users can explore the journeys of historical objects, engage in conversations with them, and discover how facts and imagination blend to create a unique experience.  

## About the Project  

This project was developed as part of a university project for a **Digital Humanities** course. The goal is to explore the intersection of generative AI and cultural heritage by offering a new, interactive way to engage with history. It aims to make museum pieces more relatable and engaging through storytelling and conversation.  

## How It Works  

- Users can search for artifacts via the **Europeana API**, which retrieves metadata and images.  
- To ensure more predictable and relevant results, the search is currently restricted to three selected museums, offering a diverse range of artifacts.  
- A pre-trained language model is used to generate a first-person narrative based on the artifact's metadata.  
- Additional factual information is gathered from the artifact‘s webpage, if available.  
- Users can chat with the artifact to learn more about its history and cultural significance.  
- The application is built with **Streamlit** to offer an intuitive user interface.

## Future Enhancements

Potential improvements include:

- Expanding artifact sources accross and beyond Europeana
- Refining narrative accuracy with improved data sources
- Paying special attention to sensitive arteficts and how to represent them respectfully
- Enhancing user interaction with multimedia elements like audio or video

## Hosted App

Try the app on Streamlit Community Cloud:
https://pastvoicesai.streamlit.app

You will need to provide access to an OpenAI API compatible model in the Settings.

## Local Installation  

To run the project locally, you need to provide a model as well as a valid API-key for Europeana.

1. Clone the repository 
   ```bash
   git clone https://github.com/katzmo/PastVoicesAI.git
   cd PastVoicesAI
   ```

2. Install dependencies
   Run pip in a virtual python environment, or use another package manager of your choice.
   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys in a new file ``.streamlit/secrets.toml``
   ```toml
   # Europeana API
   EUROPEANA_API_KEY = "your-api-key"
   # OpenAI API
   OPENAI_BASE_URL = "https://api.openai.com/v1"
   OPENAI_API_KEY = "my-openai-key"
   ```
   The model API only needs to be compatible with OpenAI, you are not required to use OpenAI!

4. Run the streamlit application
   ```bash
   streamlit run app.py
   ```

## Disclaimer  

This project is an experimental student work and is not intended to provide historically verified information. The AI-generated content is based on available data and creative storytelling, meaning some details may not be historically accurate. The focus is on users engaging with cultural heritage objects in a playful way and having fun testing different AI models, responses should not be taken too seriously. 


