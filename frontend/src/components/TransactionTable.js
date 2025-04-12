import React, { useEffect, useState } from 'react';
import './TransactionTable.css';

const TransactionTable = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    fetch('/api/all', {
      credentials: 'include', // for session-auth
    })
      .then(res => res.json())
      .then(data => setTransactions(data))
      .catch(err => console.error('Failed to fetch transactions:', err));
  }, []);

  const income = transactions
    .filter(t => t.type === 'cash_in')
    .reduce((sum, t) => sum + parseFloat(t.amount), 0);

  const expense = transactions
    .filter(t => t.type === 'cash_out')
    .reduce((sum, t) => sum + parseFloat(t.amount), 0);

  const savings = income - expense;

  return (
    <div className="transaction-container">
      <h2>Your Transactions</h2>
      <table className="transaction-table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Subtype</th>
            <th>Amount</th>
            <th>Description</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((t, index) => (
            <tr key={index}>
              <td>{t.type.replace('_', ' ').toUpperCase()}</td>
              <td>{t.subtype}</td>
              <td>${parseFloat(t.amount).toFixed(2)}</td>
              <td>{t.description || '-'}</td>
              <td>{new Date(t.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="summary">
        <p><strong>Total Income:</strong> ${income.toFixed(2)}</p>
        <p><strong>Total Expense:</strong> ${expense.toFixed(2)}</p>
        <p><strong>Savings:</strong> ${savings.toFixed(2)}</p>
      </div>
    </div>
  );
};

export default TransactionTable;
