# LLM Literature Explorer

A tool for exploring the intersection of large language models (LLMs) and literature - collecting resources, projects, and research in this fascinating interdisciplinary space.

## 🌟 Overview

This project aims to help researchers, writers, and AI enthusiasts discover interesting projects at the intersection of language models and literature. The tool searches for GitHub repositories that focus on topics such as:

- Literary analysis with LLMs
- Computational literary criticism
- AI storytelling and poetry generation
- Text generation for creative writing
- Stylistic analysis of literature using NLP

## 🛠️ Features

- Search for repositories using specialized queries
- Save search results as structured JSON
- Analyze repositories by language, topics, stars, and more
- Generate insights about trends in the LLM-literature space

## 📊 Installation and Usage

### Requirements

- Python 3.6+
- `requests` library

### Setup

1. Clone the repository:
```bash
git clone https://github.com/henrygabriels/llm-literature-explorer.git
cd llm-literature-explorer
```

2. Install dependencies:
```bash
pip install requests
```

3. (Optional) Set up a GitHub token:
For better rate limits, create a GitHub personal access token and either:
- Pass it with the `--token` argument
- Set it as an environment variable: `export GITHUB_TOKEN=your_token_here`

### Running the Tool

Basic usage:
```bash
python llm_literature_search.py
```

With analysis:
```bash
python llm_literature_search.py --analyze
```

Customize your search:
```bash
python llm_literature_search.py --page 2 --per-page 50 --output custom_results.json --analyze
```

## 📋 Example Output

The tool saves results in JSON format:

```json
[
  {
    "id": 123456789,
    "name": "literary-gpt",
    "full_name": "username/literary-gpt",
    "html_url": "https://github.com/username/literary-gpt",
    "description": "Analyzing literary texts with GPT models",
    "created_at": "2023-01-15T12:30:45Z",
    "updated_at": "2023-05-20T09:12:34Z",
    "language": "Python",
    "stargazers_count": 120,
    "forks_count": 25,
    "topics": ["nlp", "literature", "gpt", "text-analysis"]
  },
  ...
]
```

## 🔍 Analysis Features

When run with the `--analyze` flag, the tool generates:

- Distribution of programming languages
- Most common topics and tags
- Repository creation timeline
- Stars distribution

## 🤝 Contributing

Contributions welcome! Feel free to:
- Submit issues for bugs or feature requests
- Create pull requests to improve the codebase
- Suggest new search strategies or analysis methods

## 📜 License

MIT License - See LICENSE file for details

---

*This project was created to explore the fascinating space where AI language models meet literary analysis and creative writing.*
