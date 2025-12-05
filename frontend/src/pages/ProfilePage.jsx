import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API } from '../api';
import './Profile.css';

export default function ProfilePage() {
  const [user, setUser] = useState({
    email: '',
    name: ''
  });
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    // Get user info from localStorage or fetch from API
    const email = localStorage.getItem('email');
    const name = localStorage.getItem('name');

    if (email) {
      setUser({ email, name: name || 'Not set' });
      setLoading(false);
    } else {
      // Fetch user profile from API
      fetchUserProfile();
    }
  }, [navigate]);

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get(`${API}/auth/profile`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setUser({
        email: res.data.email,
        name: res.data.name || 'Not set'
      });
    } catch (err) {
      console.error('Error fetching profile:', err);
      // If token is invalid, redirect to login
      if (err.response?.status === 401) {
        handleLogout();
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    localStorage.removeItem('name');
    localStorage.removeItem('userId');
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="profile-container">
        <div className="profile-card">
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-card">
        <div className="profile-header">
          <h2>User Profile</h2>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>

        <div className="profile-content">
          <div className="profile-avatar">
            <div className="avatar-circle">
              {user.name ? user.name.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
            </div>
          </div>

          <div className="profile-info">
            <div className="info-item">
              <label>Name</label>
              <p>{user.name || 'Not set'}</p>
            </div>

            <div className="info-item">
              <label>Email</label>
              <p>{user.email}</p>
            </div>
          </div>

          <div className="profile-actions">
            <p className="welcome-message">
              Welcome to Moodlet! Start recognizing music and discover your mood.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}