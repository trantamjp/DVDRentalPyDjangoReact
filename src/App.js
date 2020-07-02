import React from 'react';
import Navigation from './AppNavigation';
import Main from './App/Main';
import styled from 'styled-components'

const Styles = styled.div`
  margin: 0 auto;
  padding: 20px;

`

const App = () => (
  <Styles>
      <h1>Python Django ORM-React Demo</h1>
      <Navigation />
      <Main />
  </Styles>
);


export default App;
