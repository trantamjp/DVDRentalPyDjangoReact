import React from 'react';
import { Switch, Route } from 'react-router-dom';
import Home from './Home';
import CustomerTable from './Customer';
import FilmTable from './Film';

const APIBASEURL = process.env.REACT_APP_APIBASEURL || (window.location.protocol + "//" + window.location.hostname + ":5007");
const CUSTOMER_API_URL = APIBASEURL + "/api/datatable/customers";
const FILM_API_URL = APIBASEURL + "/api/datatable/films";

const Main = () => (
  <Switch>
    <Route exact path='/customers' component=
      {
        () => {
          return <CustomerTable customerApiUrl={CUSTOMER_API_URL} />
        }
      }>
    </Route>
    <Route exact path='/films' component=
      {
        () => {
          return <FilmTable filmApiUrl={FILM_API_URL} />
        }
      }>
    </Route>
    {/* Anything else */}
    <Route component={
      () => {
        return <Home customerApiUrl={CUSTOMER_API_URL} filmApiUrl={FILM_API_URL} />
      }
    }></Route>
  </Switch>
);

export default Main;
