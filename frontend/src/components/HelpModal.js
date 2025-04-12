import './HelpModal.css';
import React, { useState } from 'react';
const HelpModal = ({ onClose }) => {
    return (
      <div className="modal-overlay">
        <div className="modal">
          <h2>Submit a Query</h2>
  
          {/* mailto-based form */}
          <form
            action="mailto:talha.ridwan@g.bracu.ac.bd"
            method="POST"
            encType="text/plain"
          >
            <input type="text" name="Name" placeholder="Your Name" required />
            <input type="email" name="Email" placeholder="Your Email" required />
            <textarea name="Query" placeholder="Describe your issue" rows="5" required></textarea>
  
            <div className="modal-actions">
              <button type="submit">Send</button>
              <button type="button" onClick={onClose} className="cancel">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    );
  };
  