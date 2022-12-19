import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import Root from './routes/root';
import Maneuver from './routes/maneuver';
import ErrorPage from './error-page-route'

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

// finished some of the tut
//https://reactrouter.com/en/main/start/tutorial
const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/setspeed",
    element: <App />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/maneuver",
    element: <Maneuver />,
    errorElement: <ErrorPage />,
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
//reportWebVitals();
