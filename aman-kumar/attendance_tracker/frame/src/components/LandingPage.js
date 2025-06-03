import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';
import landingImg from '../assets/landing-illustration.svg';

const LandingPage = () => {
  const fullTitle = 'Welcome to GyanSys Attendance Tracker';
  const [index, setIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const [typedTitle, setTypedTitle] = useState('');

  useEffect(() => {
    let timer;
    if (!isDeleting && index <= fullTitle.length) {
      timer = setTimeout(() => {
        setTypedTitle(fullTitle.substring(0, index));
        setIndex(index + 1);
      }, 80);
    } else if (isDeleting && index >= 0) {
      timer = setTimeout(() => {
        setTypedTitle(fullTitle.substring(0, index));
        setIndex(index - 1);
      }, 50);
    }

    if (index === fullTitle.length + 1) {
      setIsDeleting(true);
      setIndex(index - 1);
    } else if (isDeleting && index === -1) {
      setIsDeleting(false);
      setIndex(0);
    }

    return () => clearTimeout(timer);
  }, [index, isDeleting, fullTitle]);

  return (
    <>
      <div className="landing-container animated-bg">
        <nav className="landing-nav">
          <div className="logo">Attendance Tracker</div>
          <div className="nav-links">
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/register" className="nav-link">Register</Link>
          </div>
        </nav>
        <main className="landing-main">
          <section className="landing-info">
            <h1 className="animated-title typing-title">{typedTitle}<span className="typing-cursor">|</span></h1>
            <p className="animated-desc">
              Effortlessly manage, track, and analyze attendance for your organization. 
              Secure, modern, and easy to use.
            </p>
            <div className="cta-buttons">
              <Link to="/login" className="cta-btn">Get Started</Link>
              <Link to="/register" className="cta-btn secondary">Register</Link>
            </div>
          </section>
          <section className="landing-image">
            <img src={landingImg} alt="Attendance Tracker Illustration" />
          </section>
        </main>
      </div>
    </>
  );
};

export default LandingPage;
