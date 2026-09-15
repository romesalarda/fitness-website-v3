# Fitness Website V3

> **Deprecated:** This is an old project and is no longer actively maintained. The details below document the features that were implemented at the time.

## Features

- User registration, login, logout, and profile management
- Dashboard for accessing personal workouts
- Workout creation and editing
- Exercises with configurable sets, repetitions, duration, rest periods, distance, weight, and units
- Exercise metadata including target area, difficulty level, movement direction, and categories
- Superset support for grouping exercises
- Preset and public exercises/supersets that can be copied into personal workouts
- Workout session data with exercises, supersets, rest periods, and completion-oriented set tracking
- React Query data fetching and caching between the frontend and API

## Project Structure

- `frontend/` - React application using React Router and Material UI
- `backend/` - Django and Django REST Framework API

## Running Locally

The project is split into separate frontend and backend applications. Start the Django API from `backend/`, then start the React application from `frontend/`:

```bash
# backend
python manage.py runserver

# frontend
npm install
npm start
```

The frontend runs at `http://localhost:3000` by default.
