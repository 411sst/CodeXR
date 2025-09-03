# CodeXR - AR/VR Coding Assistant

An AI-powered coding assistant designed specifically for AR/VR developers working with Unity, Unreal Engine, and shaders. Built in 3 days as a complete MVP with real AI integration.

## Features

- **Task Decomposition**: Breaks complex queries into step-by-step subtasks
- **Ready-to-Paste Code**: Complete, working code snippets in Unity C#, Unreal C++, or HLSL
- **Best Practices**: Highlights common pitfalls and optimization tips
- **Web Search Integration**: Grounds responses in real documentation (DuckDuckGo)
- **Multiple AI Backends**: Mock mode, Ollama (local), or Hugging Face (online)
- **Structured Output**: JSON format for integration with other tools
- **AR/VR Focused**: Specialized for Unity XR, Unreal VR, and shader development

## Architecture

```
CodeXR/
├── app.py                 # Main Streamlit application
├── core/
│   ├── llm_handler.py     # LLM integration (Ollama/HF/Mock)
│   ├── search_agent.py    # DuckDuckGo search integration
│   ├── classifier.py      # Query classification
│   └── schemas.py         # Pydantic response schemas
├── ui/
│   └── components.py      # Streamlit UI components
├── requirements.txt       # Dependencies
└── demo/                  # Screenshots and examples
```

## Quick Start

### Prerequisites
- Python 3.8+
- (Optional) Ollama for local AI

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/codexr.git
cd codexr
```

2. **Set up virtual environment:**
```bash
python -m venv codexr_env
source codexr_env/bin/activate  # On Windows: codexr_env\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
streamlit run app.py
```

5. **Open browser to:** `http://localhost:8501`

## AI Backend Options

### Mock Mode (Default)
- Works immediately - no setup required
- Perfect for demos - instant, professional responses
- 3 detailed scenarios pre-built

### Ollama (Recommended for Real AI)
```bash
# Install Ollama from https://ollama.ai
ollama pull codellama:7b-code
# Then select "Ollama (Local)" in the app
```

### Hugging Face (Online)
- Create account at huggingface.co
- Get free API token
- Select "Hugging Face (Online)" in the app

## Usage Examples

### Unity VR Development
**Query:** "How do I add teleport locomotion in Unity VR?"

**Response:**
- 5 step-by-step tasks
- Complete C# implementation
- Best practices for VR UX
- Official Unity documentation links
- Estimated time: 45-60 minutes

### Unreal Engine VR
**Query:** "How do I set up multiplayer in Unreal VR?"

**Response:**
- Network replication setup
- Complete C++ VR character code
- Performance optimization tips
- Unreal Engine documentation
- Estimated time: 3-5 hours

### Shader Development
**Query:** "Which shader works best for AR occlusion?"

**Response:**
- AR-optimized HLSL shader code
- Mobile performance considerations
- AR Foundation integration
- Unity shader documentation
- Estimated time: 2-4 hours

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Integration**: Ollama, Hugging Face Transformers
- **Web Search**: DuckDuckGo (free, no API key required)
- **Data Validation**: Pydantic schemas
- **Styling**: Custom CSS with responsive design

## Project Goals (Achieved)

### Phase 1 MVP (Completed in 3 days):
- Assistant produces structured subtasks and code snippets
- Results grounded in real documentation via web search
- Outputs include best practices + docs links + difficulty rating
- Streamlit UI demo-ready with 3 working scenarios
- Free operation - no API costs required

### Future Enhancements (Phase 2-3):
- RAG-lite documentation retrieval
- Error debugging mode
- VS Code extension
- Voice input support

## Success Metrics

**Quantitative Results:**
- **Response Time**: <1s (Mock), 10-30s (Ollama)
- **Code Quality**: Production-ready, copy-paste ready
- **Coverage**: Unity, Unreal, Shaders, General AR/VR
- **Documentation**: 100% responses include official docs links
- **Cost**: $0 - completely free operation

**Qualitative Results:**
- **Developer Experience**: Professional UI with clear feedback
- **Accuracy**: Context-aware responses for specific platforms
- **Usability**: One-click demo scenarios for quick testing
- **Extensibility**: Modular architecture for easy enhancement

## Development & Testing

### Run Tests
```bash
python test_demo.py
```

### Launch with Alternative Script
```bash
python run.py
```

### Project Structure
- **Core Logic**: Query classification, LLM integration, web search
- **UI Components**: Streamlit-based responsive interface
- **Testing**: Automated tests for core functionality

## System Requirements

### Minimum:
- Python 3.8+
- 4GB RAM
- Internet connection (for web search)

### Recommended:
- Python 3.11+
- 8GB+ RAM (for Ollama)
- Multi-core CPU
- Linux/macOS/Windows

## Troubleshooting

### Common Issues:

**Ollama not connecting:**
```bash
ollama serve
ollama pull codellama:7b-code
```

**DuckDuckGo search fails:**
```bash
pip install --upgrade ddgs
```

**Streamlit issues:**
```bash
streamlit cache clear
```

### Performance Tips:
- Use Mock mode for fastest demos
- Ollama first response is slower (model loading)
- CPU-only inference works fine for development

## Contributing

1. Fork the repository
2. Create a feature branch 
3. Commit your changes 
4. Push to the branch 
5. Open a Pull Request

### Development Guidelines:
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation as needed
- Ensure backward compatibility


## Acknowledgments

- **Unity Technologies** - XR Interaction Toolkit documentation
- **Epic Games** - Unreal Engine VR resources  
- **Ollama Team** - Local LLM inference
- **Streamlit** - Rapid web app development
- **DuckDuckGo** - Free web search API

## Roadmap

### Phase 2 (Next Sprint):
- RAG-lite documentation indexing
- Error log debugging mode
- Voice input with Whisper
- Enhanced mobile responsiveness

### Phase 3 (Future):
- VS Code extension
- Real-time collaboration features
- Custom model fine-tuning
- Plugin ecosystem
