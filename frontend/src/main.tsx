import React from 'react';
import ReactDOM from 'react-dom/client';

import '@andritzot/metris-web-ui/styles.css';

import { MetrisUIProvider } from '@andritzot/metris-web-ui/context';
import { useTheme } from '@andritzot/metris-web-utils/store/useTheme';


import App from './App';

useTheme.getState().switchTheme("light");

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <MetrisUIProvider language="en">
            <App />
        </MetrisUIProvider>
    </React.StrictMode>
);