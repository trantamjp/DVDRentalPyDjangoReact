import React from 'react';
import { NavLink } from 'react-router-dom';
import './AppNavigation.css';

const Navigation = () => (
  <nav>
    <ul>
      <li><NavLink activeClassName="current" to='/home'>Home</NavLink></li>
      <li><NavLink activeClassName="current" to='/customers'>Customer</NavLink></li>
      <li><NavLink activeClassName="current" to='/films'>Film</NavLink></li>
    </ul>
  </nav>
);

export default Navigation;
