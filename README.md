# Ohmni Oracle

This project processes various types of architectural and engineering drawings, including electrical, mechanical, plumbing, and architectural documents. It uses PyMuPDF for general text extraction, with specialized Azure Document Intelligence processing for electrical panel schedules, and GPT-4o-mini for data structuring.

## Features

- Intelligent document processing:
  - PyMuPDF for general drawing text extraction
  - Azure Document Intelligence for electrical panel schedules
  - GPT-4o-mini for structured data generation
- Smart detection of electrical panel schedules
- Asynchronous batch processing of multiple drawings
- Specialized templates for different drawing types
- Comprehensive error handling and logging
- Test suite for validation
- Support for multiple document types:
  - Architectural drawings
  - Electrical drawings (with specialized panel schedule processing)
  - Mechanical drawings
  - Plumbing drawings

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with required credentials:
```env
DI_KEY=your_azure_key
DI_ENDPOINT=your_azure_endpoint
OPENAI_API_KEY=your_api_key_here
```
4. Ensure you have the necessary JSON templates in the `templates` folder:
- `a_rooms_template.json`
- `e_rooms_template.json`

## File Structure

- `main.py`: Asynchronous PDF processing coordinator with batch processing capabilities
- `.env`: Environment variables (Azure and OpenAI credentials)
- `.gitignore`: Comprehensive Git ignore rules for Python projects
- `.cursorrules`: Cursor editor configuration with AI/ML processing rules
- `git-best-practices-guide.md`: Detailed Git workflow and best practices
- `requirements.txt`: Project dependencies including Azure AI and document processing packages

### Config
- `config/.gitignore`: Environment-specific ignore rules
- `config/settings.py`: Centralized configuration for Azure and processing settings

### Templates
- `templates/room_templates.py`: Room data processing and template management
- `templates/a_rooms_template.json`: Architectural room data schema
- `templates/e_rooms_template.json`: Electrical room data schema

### Utils
- `utils/__init__.py`: Package initialization
- `utils/document_processor.py`: Base Azure Document Intelligence processor
- `utils/drawing_processor.py`: Specialized drawing processing with Azure integration
- `utils/file_utils.py`: File system operations and folder management
- `utils/pdf_processor.py`: PDF processing with Azure and PyMuPDF fallback
- `utils/pdf_utils.py`: Advanced PDF utilities for text and image extraction

### Tests
- `tests/__init__.py`: Test package initialization
- `tests/test_processor.py`: Drawing processor test suite

### Documents
- `documents/proj-work-flow.md`: System workflow documentation

## Folder Structure
ohmni_oracle/
├── config/
│   ├── .gitignore
│   └── settings.py
├── documents/
│   └── proj-work-flow.md
├── templates/
│   ├── __pycache__/
│   ├── a_rooms_template.json
│   ├── e_rooms_template.json
│   └── room_templates.py
├── tests/
│   ├── __init__.py
│   └── test_processor.py
├── utils/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── drawing_processor.py
│   ├── file_utils.py
│   ├── pdf_processor.py
│   └── pdf_utils.py
├── venv/
├── .cursorrules
├── .env
├── .gitignore
├── git-best-practices-guide.md
├── main.py
├── README.md
└── requirements.txt