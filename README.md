# Moviditor

An undeployed website for editing videos, built using Moviepy, Django, HTML, and Bootstrap5.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Description

Moviditor is a web-based application designed for video editing. It leverages the power of Moviepy for video processing, Django for the backend, and HTML and Bootstrap5 for the frontend. Currently, the application is not deployed.

## Features

- Video editing using Moviepy
- Backend developed with Django
- Responsive frontend using Bootstrap5

## Installation

To get a local copy up and running, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/CrusaderGoT/Moviditor.git
   cd Moviditor
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Django migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Usage

To start using Moviditor, navigate to `http://127.0.0.1:8000/` in your web browser after starting the development server. You can upload videos and use the available tools to edit them.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is currently not licensed.
---
