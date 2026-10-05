import React from 'react';
import { createRoot } from 'react-dom/client';
import PublicApp from './PublicApp';

createRoot(document.getElementById('root')!).render(<React.StrictMode><PublicApp /></React.StrictMode>);
