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
import Dashboard from './pages/dashboard/Dashboard';
import WorkoutBuilder from './pages/builder/WorkoutBuilder';

import NavigationBar from './components/NavigationBar'
// react query
import { QueryClientProvider, QueryClient } from 'react-query'
import { ReactQueryDevtools } from 'react-query/devtools'


const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
});

ReactDOM.render(
  <Router>
    <QueryClientProvider client={queryClient}>
      <React.StrictMode>
        <NavigationBar />
        <Routes>
          <Route exact path="/" element={<App />} />

          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/register" element={<Register />} />
          <Route path="/my-profile" element={<Profile />} />
          <Route path="/dashboard" element={<Dashboard />} />

          <Route path="/my-workouts/:uuid/edit" element={<WorkoutBuilder />} />
          {/* <Route path="/my-workouts/create-workout" element={<CreateWorkoutView />} /> */}

        </Routes>
      </React.StrictMode>
      <ReactQueryDevtools />
    </QueryClientProvider>
  </Router>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
