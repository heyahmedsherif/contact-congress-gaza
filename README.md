# Contact Congress for Gaza and Justice

A Streamlit application that helps users contact their congressional representatives about Gaza-related issues. The app allows users to:

- Find their representatives using ZIP code
- Select specific issues to discuss
- Generate personalized contact scripts
- Get direct contact information for representatives

## Features

- ZIP code-based representative lookup using 5 Calls API
- Personalized script generation
- Support for multiple issues:
  - Ceasefire in Gaza
  - Condemning ethnic cleansing proposals
  - Humanitarian aid access
  - Military aid concerns
- Contact information for representatives' offices

## Setup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your 5 Calls API key:
```
FIVE_CALLS_API_KEY=your_api_key_here
```

4. Run the app:
```bash
streamlit run app.py
```

## Deployment

This app is deployed on Streamlit Cloud. You can access it at [your-app-url].

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 