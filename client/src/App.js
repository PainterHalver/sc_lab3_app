import './App.css';

import {
  BrowserRouter,
  Link,
  Route,
  Routes
} from "react-router-dom";
import CSVList from './components/CSVList';
import CheckSecurityGroups from './components/CheckSecurityGroups';

function App() {
  return (
    <BrowserRouter>
      <div className='flex flex-col min-h-screen'>
        <nav className="w-full bg-[#E9A89B] h-20 flex justify-center items-center gap-3">
          <Link to={'/'}><button className="btn btn-warning">Check Security Groups</button></Link>
          <Link to={'/csv'}><button className="btn btn-warning">CSV List</button></Link>
        </nav>
        <body className='flex-grow bg-[#FFEBB2] flex flex-col items-center p-5'>
          <Routes>
            <Route path='/' element={<CheckSecurityGroups />} />
            <Route path='/csv' element={<CSVList />} />
          </Routes>
        </body>
      </div>
    </BrowserRouter>
  );
}

export default App;
