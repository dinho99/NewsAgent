# AI News Aggregator

This project implements an AI-powered workflow for summarizing and aggregating news about Italian politics. The workflow leverages multiple language models (LLMs) and the Brave Search API to create a comprehensive and multilingual summary.

## Workflow Overview

1. **Input Prompts**: The user provides two prompts:
   - One in Italian
   - One in English

2. **Language Model Processing**:
   - The Italian prompt is processed by an LLM focused on Italian news sources.
   - The English prompt is processed by an LLM focused on international news sources.

3. **News Search**:
   - Both LLMs use the Brave Search API to retrieve the latest news about Italian politics from relevant sources.

4. **Summarization**:
   - Each LLM summarizes the retrieved news into distinct content:
     - One summary in Italian
     - One summary in English

5. **Translation**:
   - The English summary is translated into Italian using another LLM.

6. **Aggregation**:
   - Both summaries (original Italian and translated Italian) are passed to an "aggregator" LLM.
   - The aggregator extracts key information from both summaries and creates a unified final output in Italian.

## Features

- **Multilingual Support**: Combines insights from international and local news sources.
- **Automated Translation**: Ensures consistency by translating content for unified processing.
- **Custom Aggregation**: The final summary highlights the most relevant information from both perspectives.

## Dependencies

- Python 3.8+
- [OpenAI API](https://openai.com/api/)
- [Brave Search API](https://brave.com/search/)
- Required Python libraries (listed in `requirements.txt`):
  - `openai`
  - `requests`
  - `dotenv`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dinho99/ai-news-aggregator.git
   cd ai-news-aggregator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your API keys:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     BRAVE_SEARCH_API_KEY=your_brave_search_api_key
     ```
     
## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve this project.
