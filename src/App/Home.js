import React from 'react';
import styled from 'styled-components'

function CustomerAPIClick() {
    document.forms["formCustomerAPI"].submit();
}

function FilmAPIClick() {
    document.forms["formFilmAPI"].submit();
    return false;
}

const Styles = styled.div`
span.link {
    cursor: pointer;
    text-decoration: underline;
}
`

const Home = (props) => (
    <Styles>
        <h2>Github</h2>
        <a href="https://github.com/trantamjp/DVDRentalPyDjangoReact" target="_blank" rel="noopener noreferrer">
            https://github.com/trantamjp/DVDRentalPyDjangoReact</a>
        <h2>Sample Data</h2>
        <h4>Download from here <a href="https://www.postgresqltutorial.com/postgresql-sample-database/" target="_blank" rel="noopener noreferrer">
            https://www.postgresqltutorial.com/postgresql-sample-database/</a></h4>
        <p>Please click the link from the top menu</p>
        <ol>
            <li>
                <form id="formCustomerAPI" action={props.customerApiUrl} method="POST" target="_blank"></form>
                <p>Customer List</p>
                <p>DataTable with server-side processing, pulling customer data from the API <span className="link" onClick={CustomerAPIClick}>here</span> (showing first 10 rows without parameters).
                </p>
            </li>
            <li>
                <form id="formFilmAPI" action={props.filmApiUrl} method="POST" target="_blank"></form>
                <p>Films List</p>
                <p>DataTable with server-side processing, pulling customer data from the API <span className="link" onClick={FilmAPIClick}>here</span> (showing first 10 rows without parameters).
                </p>
            </li>
        </ol>
    </Styles>
);

export default Home;
