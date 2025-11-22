# 🤖 AI Recipe Creator 🍳

A smart web application that transforms images of ingredients into **delicious recipes** using artificial intelligence. Built with **Flask** and **Google's Gemini AI**, this tool helps home cooks and food enthusiasts discover new culinary creations from whatever ingredients they have on hand.

---

## ✨ Features

* **Image Analysis**: Upload a photo of your ingredients for **AI-powered identification**.
* **Smart Recipe Generation**: Creates detailed, unique recipes based on detected ingredients.
* **Dietary Customization**: Accommodates **vegetarian, gluten-free, low-carb** preferences.
* **Multiple Format Support**: Handles JPEG, PNG, WEBP, GIF, and BMP images.
* **Real-time Processing**: Live progress indicators during AI generation.
* **Export Options**: Easily copy recipes or **download as Markdown files**.
* **Responsive Design**: Works seamlessly on desktop and mobile devices.

---

## 🛠️ Tech Stack

### Backend
* **Python** with **Flask**
* **Google Gemini AI** for intelligence
* **Pillow** for image processing
* **Gunicorn** production server

### Frontend
* **Vanilla JavaScript**
* Modern **CSS** with glassmorphism design
* **Marked.js** for Markdown rendering
* Drag-and-drop file API

### Deployment
* **Render** cloud platform
* Environment-based configuration

---

## 🚀 Quick Start

### Prerequisites

* **Python 3.8+**
* **Google Gemini API key**

### Local Development

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/recipe-creator.git](https://github.com/yourusername/recipe-creator.git)
    cd recipe-creator
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables**
    Create a file named `.env` and add your API key:
    ```bash
    echo "GEMINI_API_KEY=your_api_key_here" > .env
    ```

4.  **Run the application**
    ```bash
    python app.py
    ```
    Open `http://localhost:5000` in your browser.

### Deployment on Render

This project is configured for easy deployment on Render.

1.  **Fork** this repository.
2.  Create a new **Web Service** on Render.
3.  Connect your GitHub repository.
4.  Add your `GEMINI_API_KEY` as an **environment variable**.
5.  Deploy!

---

## 💡 How It Works

1.  **Upload**: User uploads an image of ingredients via drag-and-drop or file selection.
2.  **Process**: Server validates image format and converts it to an optimal size.
3.  **Analyze**: Google Gemini AI identifies ingredients and processes dietary preferences.
4.  **Generate**: AI creates a unique recipe using *only* the identified ingredients.
5.  **Display**: The formatted recipe appears with proper Markdown styling.


---

## 📂 Project Structure

```text
recipe-creator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── runtime.txt            # Python version specification
├── render.yaml            # Render deployment configuration
└── templates/
    └── index.html         # Frontend interface
---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit **pull requests**, report bugs, or suggest new features.

1.  **Fork** the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👤 Developer

Created by **Gaurav Dhangar** – demonstrating full-stack development with AI integration and modern web technologies.
