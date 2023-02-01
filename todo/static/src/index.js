/* @odoo-module */

// import React from 'react';
// import ReactDOM from 'react-dom/client';
// https://reactjsexample.com/to-do-list-app-created-with-react-library-with-react-class-and-functional-components/
import TodoContainer from './components/TodoContainer';

window.useState = React.useState;
const root = ReactDOM.createRoot(document.getElementById('todos-example'));
root.render(
  <React.StrictMode>    
    <TodoContainer />    
  </React.StrictMode>,
);