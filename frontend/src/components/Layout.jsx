// frontend/src/components/Layout.jsx
import React from 'react';
import Head from 'next/head';
import { UI_DEFAULT_PAGE_TITLE } from '../utils/constants';

const Layout = ({ children, title = UI_DEFAULT_PAGE_TITLE }) => {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="description" content="Todo App with AI Chat Assistant" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="layout-container">
        <header className="layout-header">
          <h1>{title}</h1>
        </header>
        <main className="layout-main">{children}</main>
        <footer className="layout-footer">
          <p>© {new Date().getFullYear()} Todo App with AI Assistant</p>
        </footer>
      </div>
      <style jsx global>{`
        body {
          margin: 0;
          padding: 0;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
            Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
          background-color: #f5f5f5;
        }
        
        .layout-container {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
        }
        
        .layout-header {
          background-color: #fff;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          padding: 1rem;
          text-align: center;
        }
        
        .layout-main {
          flex: 1;
          padding: 1rem;
          max-width: 1200px;
          margin: 0 auto;
          width: 100%;
        }
        
        .layout-footer {
          background-color: #fff;
          padding: 1rem;
          text-align: center;
          border-top: 1px solid #eee;
        }
      `}</style>
    </>
  );
};

export default Layout;