import React from 'react'
import styled from 'styled-components'
import { useTable, usePagination, useSortBy, useFilters } from 'react-table'

const Styles = styled.div`
  padding: 1rem;

  table {
    border-spacing: 0;
    border: 1px solid black;

    tr {
      :last-child {
        td {
          border-bottom: 0;
        }
      }
    }

    th {
      .sorting_both {
        background-image: url("images/sort_both.png");
        background-repeat: no-repeat;
        background-position: center right;  
      }
      .sorting_asc {
        background-image: url("images/sort_asc.png");
        background-repeat: no-repeat;
        background-position: center right;  
      }
      .sorting_desc {
        background-image: url("images/sort_desc.png");
        background-repeat: no-repeat;
        background-position: center right;  
      }  
    }
  
    th,
    td {
      margin: 0;
      padding: 0.5rem 1rem;
      border-bottom: 1px solid black;
      border-right: 1px solid black;

      :last-child {
        border-right: 0;
      }
    }
  }

  .pagination {
    padding: 0.5rem;
  }
`

function actionBoolFilter({ column: { filterValue, Header, setFilter } }) {
  return (
    <select onClick={e => { e.stopPropagation(); }} onChange={e => { setFilter(e.target.value || undefined); }}>
      <option value="">*</option>
      <option value="1">active</option>
      <option value="0">Non active</option>
    </select>
  );
}

// Define a default UI for filtering
function DefaultColumnFilter({ column: { filterValue, Header, setFilter } }) {

  return (
    <input
      value={filterValue || ""}
      onChange={e => {
        setFilter(e.target.value || undefined); // Set undefined to remove the filter entirely
      }}
      onClick={e => { e.stopPropagation(); }}
      placeholder={`Search ${Header}`}
    />
  );
}

// Let's add a fetchData method to our Table component that will be used to fetch
// new data when pagination state changes
// We can also add a loading state to let our table know it's loading new data
function Table({
  columns: originalColumns,
  apiData,
  fetchData,
  loading,
}) {
  const defaultColumn = React.useMemo(
    () => ({
      // Let's set up our default Filter UI
      Filter: DefaultColumnFilter
    }),
    []
  );

  if (!apiData.hasOwnProperty('data')) {
    apiData['data'] = [];
  }

  const controlledPageCount = apiData['pageCount'] || 0;

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    page,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    allColumns,
    // Get the state from the instance
    state: { pageIndex, pageSize, filters, sortBy },
  } = useTable(
    {
      columns: originalColumns,
      data: apiData.data,
      defaultColumn,
      initialState: { pageIndex: 0, pageSize: 10 },
      manualPagination: true,
      pageCount: controlledPageCount,
      manualFilters: true,
      manualSortBy: true,
    },
    useFilters,
    useSortBy,
    usePagination,
  )

  // Listen for changes in pagination and use the state to fetch our new data
  React.useEffect(() => {
    fetchData({ allColumns, pageIndex, pageSize, filters, sortBy })
  },
    // eslint-disable-next-line
    [fetchData, pageIndex, pageSize, filters, sortBy])

  // Render the UI for your table
  return (
    <>
      <h2>Customer List</h2>
      <table {...getTableProps()}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps(
                  column.getSortByToggleProps({
                    title: 'Toggle sort by ' + column.Header
                  }),
                )}>
                  <div className={column.isSorted ? (column.isSortedDesc ? 'sorting_desc' : 'sorting_asc') : 'sorting_both'}>{column.render('Header')}</div>
                  <div>{column.canFilter ? column.render("Filter") : null}</div>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {page.map((row, i) => {
            prepareRow(row)
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => {
                  return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                })}
              </tr>
            )
          })}
          <tr>
            {
              apiData.error ? (
                <td colSpan="10000">
                  Error [{apiData.error}]
                </td>
              ) :
                loading ? (
                  // Use our custom loading state to show a loading indicator
                  <td colSpan="10000">Loading...</td>
                ) : (
                    <td colSpan="10000">
                      Showing {pageIndex * pageSize + 1} to {pageIndex * pageSize + apiData.data.length} of {apiData.recordsFiltered} entries
                      {apiData.recordsFiltered < apiData.recordsTotal ? "(filtered from " + apiData.recordsTotal + " total entries)" : ""}
                    </td>
                  )}
          </tr>
        </tbody>
      </table>
      {/* 
        Pagination
      */}
      <div className="pagination">
        <button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
          {'<<'}
        </button>{' '}
        <button onClick={() => previousPage()} disabled={!canPreviousPage}>
          {'<'}
        </button>{' '}
        <button onClick={() => nextPage()} disabled={!canNextPage}>
          {'>'}
        </button>{' '}
        <button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}>
          {'>>'}
        </button>{' '}
        <span>
          Page{' '}
          <strong>
            {pageIndex + 1} of {pageOptions.length}
          </strong>{' '}
        </span>
        <span>
          | Go to page:{' '}
          <input
            type="number"
            value={pageIndex + 1}
            onChange={e => {
              const page = e.target.value ? Number(e.target.value) - 1 : 0
              gotoPage(page)
            }}
            style={{ width: '100px' }}
          />
        </span>{' '}
        <select
          value={pageSize}
          onChange={e => {
            setPageSize(Number(e.target.value))
          }}
        >
          {[10, 20, 30, 40, 50].map(pageSize => (
            <option key={pageSize} value={pageSize}>
              Show {pageSize}
            </option>
          ))}
        </select>
      </div>
    </>
  )
}

function CustomerTable(props) {

  const customerApiUrl = props.customerApiUrl
  const columns = React.useMemo(
    () => [
      {
        Header: 'First Name',
        accessor: 'first_name',
      },
      {
        Header: 'Last Name',
        accessor: 'last_name',
      },
      {
        Header: 'Address',
        accessor: ((originalRow, rowIndex) => {
          const address = originalRow.address;
          return [address.address, address.address2].filter(addr => !!addr).join(' ');
        }),
        id: 'address.address',
      },
      {
        Header: 'City',
        accessor: 'address.city.city',
      },
      {
        Header: 'Zip Code',
        accessor: 'address.postal_code',
      },
      {
        Header: 'Country',
        accessor: 'address.city.country.country',
      },
      {
        Header: 'Phone',
        accessor: 'address.phone',
      },
      {
        Header: 'Active',
        accessor: ((originalRow, rowIndex) => {
          return originalRow.activebool ? 'active' : 'non-active'
        }),
        id: 'activebool',
        Filter: actionBoolFilter,
        filter: "includes",
      },
    ],
    []
  )

  // We'll start our table without any data
  const [apiData, setApiData] = React.useState({ data: [], recordsFiltered: 0, recordsTotal: 0 })
  const [loading, setLoading] = React.useState(false)
  const fetchIdRef = React.useRef(0)

  const fetchData = React.useCallback(({ allColumns, pageSize, pageIndex, filters, sortBy }) => {
    // Give this fetch an ID
    const fetchId = ++fetchIdRef.current;
    // Set the loading state
    setLoading(true);

    const apiSortBy = sortBy.map(entry => (
      {
        ...entry,
        sort_type: allColumns.find(col => col.id === entry.id && col.sortedIndex >= 0)["sortType"]
      }
    ));

    const apiFilters = filters.map(entry => (
      {
        ...entry,
        filter: allColumns.find(col => col.id === entry.id)['filter']
      }
    ));

    fetch(customerApiUrl,
      {
        method: 'POST',
        cache: 'no-cache',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          fetch_id: fetchId,
          limit: pageSize,
          offset: pageIndex * pageSize,
          filters: apiFilters,
          orders: apiSortBy,
        })
      }).then(res => res.json())
      .then(response => {
        if (response.fetch_id === fetchIdRef.current) {
          setApiData({
            data: response.data,
            recordsFiltered: response.records_filtered,
            recordsTotal: response.records_total,
            pageCount: Math.ceil(response.records_filtered / pageSize)
          });
          setLoading(false);
        }
      })
      .catch(function (error) {
        console.log("Fetching data", error);
        if (typeof (error) != "string") {
          error = error.toString()
        }
        setApiData({ error: error });
        setLoading(false);
      });
  },
    // eslint-disable-next-line 
    [])

  return (
    <Styles>
      <Table
        columns={columns}
        apiData={apiData}
        fetchData={fetchData}
        loading={loading}
      />
    </Styles>
  )
}

export default CustomerTable
