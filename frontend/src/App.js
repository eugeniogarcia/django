import logo from './logo.svg';
import './App.css';
import React,{ useEffect, useState } from 'react';
import axios from 'axios';

const lista = {
  todos:[
    {
      "id": 1,
      "title": "1st todo",
      "body": "Learn Django properly."
    },
    {
      "id": 2,
      "title": "Second item",
      "body": "Learn Python."
    },
    {
      "id": 3,
      "title": "Learn HTTP",
      "body": "It's important."
    }
  ]
}

const URL = 'http://localhost:8080/api/v1/'

function App() {
  const [estado, actualizaEstado] = useState(lista)
  
  function getTodos() {
    axios
      .get(URL)
      .then(res => {
        actualizaEstado({ todos: res.data });
      })
      .catch(err => {
        console.log(err);
      });
  }

  useEffect(getTodos,[])

  return (
    <div>
      {estado.todos.map(x => (
        <div key={x.id}>
          <h1>{x.title}</h1>
          <p>{x.body}</p>
        </div>
      ))}
    </div>
  );
}

export default App;
