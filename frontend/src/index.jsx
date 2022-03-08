import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
// routing
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
// auth views
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Logout from './pages/auth/Logout';
import Profile from './pages/auth/Profile';
// builder views

ReactDOM.render(
  <Router>
    <React.StrictMode>
      <Routes>
        <Route exact path="/" element={<App />} />

        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<Register />} />
        <Route path="/my-profile" element={<Profile />} />

        {/* <Route path="/my-workouts/:slug/edit" element={<EditWorkoutView />} />
        <Route path="/my-workouts/create-workout" element={<CreateWorkoutView />} /> */}

      </Routes>
    </React.StrictMode>
  </Router>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
