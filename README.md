# Viniqufy

Viniqufy is a web application that allows users to determine how unique their playlist is. By analyzing your playlist's content, Viniqufy provides insights into the diversity and rarity of the tracks you listen to.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Future Changes](#future-changes)
- [License](#license)

## Features

- **Playlist Analysis**: Analyze any playlist to determine its uniqueness based on various metrics.
- **Real-Time Results**: Get instant feedback on your playlist's uniqueness.
- **Secure Backend**: FastAPI-powered backend for reliable and secure performance.

## Technologies Used

- **Frontend**: React, Chakra UI
- **Backend**: FastAPI
- **Other Tools**:
  - Axios (for HTTP requests)
  - Spotify API (for playlist data)
  - PostgreSQL (as the database)

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/goldic342/viniqufy.git
   cd viniqufy
   ```

2. **Install frontend dependencies**:

   ```bash
   cd frontend
   npm install
   ```

3. **Install backend dependencies**:

   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Create a `.env` file in the root directory and add necessary configurations, like your Spotify API credentials see `.env.example`.

5. **Run the application**:

   - Start the backend server:

     ```bash
     fastapi dev src/app.py
     ```

   - Start the frontend server:

     ```bash
     cd ../frontend
     npm run dev
     ```

6. **Open your browser** and navigate to `http://localhost:5173`.

## Future Changes

Here are some planned features and improvements for future releases:

- **Caching**: Implement caching to reduce loading times and improve performance.
- **Beautiful UI**: Add a beautiful and intuitive user interface
- **Admin Panel**: Add an admin panel to view user data and manage the application.
- **Multiple Playlist Comparison**: Compare the uniqueness of multiple playlists at once.
- **Enhanced Analytics**: Provide deeper insights with more detailed metrics and visualizations.
- **Localization**: Add support for multiple languages to cater to a global audience.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
