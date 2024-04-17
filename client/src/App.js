import './App.css';

import {
  BrowserRouter,
  Link,
  Route,
  Routes
} from "react-router-dom";
import CSVList from './components/CSVList';
import CheckSecurityGroups from './components/CheckSecurityGroups';
import "@fontsource/inter"; // Defaults to weight 400

const routes = [
  {
    path: '/',
    component: CheckSecurityGroups,
    label: 'Check Security Groups'
  },
  {
    path: '/csv',
    component: CSVList,
    label: 'CSV List'
  }
]

function NavigationBar() {
  return (
    <nav className="flex items-center justify-center w-full h-20 bg-[--bg-primary] border-b border-[--border]">
      {routes.map(route => (
        <Link
          key={route.path}
          to={route.path}
          className={`flex items-center justify-center h-full transition-colors duration-200 ease-in-out btn min-w-56 btn-ghost btn-square rounded-none bg-[--bg-secondary] hover:bg-[--bg-secondary-hover] text-base font-bold`}
        >
          {route.label}
        </Link>
      ))}
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className='flex flex-col min-h-screen text-white'>
        <NavigationBar />
        <body className='flex-grow bg-[--bg-primary] flex flex-col items-center p-5'>
          <Routes>
            {routes.map(route => (
              <Route key={route.path} path={route.path} element={<route.component />} />
            ))}
          </Routes>
        </body>
      </div>
    </BrowserRouter>
  );
}

export default App;
