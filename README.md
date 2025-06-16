# InfoCulus

An intelligent assistant that can handle both news queries and mathematical calculations using Groq's API and NewsAPI.

## Features

- **News Search**: Get the latest news and historical news articles
- **Mathematical Calculations**: Perform complex calculations with step-by-step explanations
- **Intelligent Query Classification**: Automatically determines if a query is news-related or a calculation
- **Streaming Responses**: Real-time streaming of responses for better user experience

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

4. Run the application:
```bash
python app.py
```

## API Keys Required

- **Groq API Key**: Get it from [Groq's website](https://console.groq.com/)
- **NewsAPI Key**: Get it from [NewsAPI.org](https://newsapi.org/)

## Project Structure

```
.
├── agent/
│   ├── calculator_agent.py
│   ├── newscaster_agent.py
│   └── orchestrator.py
├── utils/
│   ├── query_classifier.py
│   └── web_search.py
├── config/
│   └── config.py
├── app.py
├── requirements.txt
└── README.md
```

## Usage

1. Start the application
2. Enter your query in the text input
3. The system will automatically:
   - Classify your query as news or calculation
   - Route it to the appropriate agent
   - Provide a detailed response

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
