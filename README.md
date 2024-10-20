

# 911 Dispatch AI

## Overview

This project utilizes Deepgram and Gemini to automate the dispatch of 911 calls when individuals are unable to do so themselves. It features a React Native front end for user interaction and a FastAPI back end for processing requests.

## Table of Contents

- [Technologies](#technologies)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Technologies

- **Frontend**: React Native
- **Backend**: FastAPI
- **AI**: Deepgram, Gemini
- **Database**: PostgreSQL (with psycopg2)
- **Tooling**: Expo CLI, ngrok

## Installation

### Backend Setup

1. **Install Python Dependencies**

   For **Linux**:
   ```bash
   pip install fastapi httpx uvicorn
