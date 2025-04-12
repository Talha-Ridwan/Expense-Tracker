import React, { useState } from 'react';
import './Navbar.css';
import HelpModal from './HelpModal';

const Navbar = () => {
  const [showHelpModal, setShowHelpModal] = useState(false);

  const handleHelp = () => {
    setShowHelpModal(true);
  };

  const handleLogout = async () => {
    try {
      const res = await fetch('/api/logout', {
        method: 'POST',
        credentials: 'include', // includes cookies/session
      });

      if (res.ok) {
        window.location.href = '/login'; // redirect to login page
      } else {
        alert('Logout failed!');
      }
    } catch (err) {
      console.error(err);
      alert('Something went wrong.');
    }
  };

  return (
    <div style={{ display: 'flex', width: '100%' }}>
      <div className="sidebar"></div>
      <nav className="navbar">
        <div className="logo">Expense Tracker</div>
        <div className="navbar-buttons">
          <button onClick={handleHelp}>Help</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      {showHelpModal && <HelpModal onClose={() => setShowHelpModal(false)} />}
    </div>
  );
};

export default Navbar;
