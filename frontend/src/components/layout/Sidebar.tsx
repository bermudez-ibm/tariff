import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { cn } from '../../lib/utils';

const navigation = [
  { name: 'Dashboard', path: '/' },
  { name: 'Policy Events', path: '/policy-events' },
  { name: 'Scenarios', path: '/scenarios' },
  { name: 'Agreements', path: '/agreements' },
  { name: 'Recommendations', path: '/recommendations' },
  { name: 'Alerts', path: '/alerts' },
  { name: 'Compliance', path: '/compliance' },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <aside className="app-sidebar bg-gray-900 text-white flex flex-col">
      <div className="p-6">
        <h1 className="text-xl font-bold">Tariff Resilience</h1>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navigation.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                'block px-3 py-2 rounded-md text-sm font-medium transition-colors',
                isActive
                  ? 'bg-gray-800 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              )}
            >
              {item.name}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
