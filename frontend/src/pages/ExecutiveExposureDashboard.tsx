import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { request } from '../lib/api-client';

interface ExposureData {
  total_exposure: number;
  material_events_30d: number;
  unresolved_high_severity: number;
  agreement_savings: number;
}

interface Alert {
  id: string;
  event: string;
  severity: string;
  exposure: string;
  affected: string;
  owner: string;
  status: string;
  days_open: number;
}

export default function ExecutiveExposureDashboard() {
  const [exposureData, setExposureData] = useState<ExposureData | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);

        // Use mock data for demo - API endpoints require additional parameters
        setExposureData({
          total_exposure: 47200000,
          material_events_30d: 23,
          unresolved_high_severity: 7,
          agreement_savings: 2100000
        });
        setAlerts([
          {
            id: 'ALT-2847',
            event: 'Vietnam tariff increase 15% → 22%',
            severity: 'critical',
            exposure: '$8.4M',
            affected: '142 SKUs, 3 suppliers',
            owner: 'Strategic Sourcing',
            status: 'unresolved',
            days_open: 12
          },
          {
            id: 'ALT-2839',
            event: 'China Section 301 expansion',
            severity: 'high',
            exposure: '$5.2M',
            affected: '87 SKUs, 2 suppliers',
            owner: 'Trade Compliance',
            status: 'in-progress',
            days_open: 8
          },
          {
            id: 'ALT-2832',
            event: 'Bangladesh GSP suspension risk',
            severity: 'high',
            exposure: '$3.1M',
            affected: '64 SKUs, 1 supplier',
            owner: 'Trade Compliance',
            status: 'in-progress',
            days_open: 15
          }
        ]);
        setError(null);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch dashboard data');
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-red-600 font-medium">Error: {error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 px-4 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-50 min-h-screen">
      <div className="max-w-[1600px] mx-auto p-8">
        <div className="mb-8">
          <h1 className="text-[28px] font-bold text-slate-900 mb-2">Executive Exposure Dashboard</h1>
          <p className="text-sm text-slate-600">Real-time visibility into tariff exposure, material events, and mitigation effectiveness</p>
        </div>

        {/* KPI Grid */}
        <div className="grid grid-cols-4 gap-5 mb-8">
          <div className="bg-white border border-slate-200 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-600 uppercase tracking-wide mb-2">Total Exposure Value</div>
            <div className="text-[32px] font-bold text-slate-900 mb-1">$47.2M</div>
            <div className="text-[13px] font-medium text-red-600 flex items-center gap-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
              </svg>
              <span>+$3.8M vs last month</span>
            </div>
          </div>
          
          <div className="bg-white border border-slate-200 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-600 uppercase tracking-wide mb-2">Material Events (30d)</div>
            <div className="text-[32px] font-bold text-slate-900 mb-1">23</div>
            <div className="text-[13px] font-medium text-red-600 flex items-center gap-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <span>+8 new events</span>
            </div>
          </div>
          
          <div className="bg-white border border-slate-200 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-600 uppercase tracking-wide mb-2">Unresolved High-Severity</div>
            <div className="text-[32px] font-bold text-slate-900 mb-1">7</div>
            <div className="text-[13px] font-medium text-red-600 flex items-center gap-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Requires attention</span>
            </div>
          </div>
          
          <div className="bg-white border border-slate-200 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-600 uppercase tracking-wide mb-2">Agreement Savings Identified</div>
            <div className="text-[32px] font-bold text-slate-900 mb-1">$2.1M</div>
            <div className="text-[13px] font-medium text-emerald-600 flex items-center gap-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              <span>+$420K this quarter</span>
            </div>
          </div>
        </div>

        {/* Content Grid */}
        <div className="grid grid-cols-3 gap-6 mb-6">
          {/* Exposure by Country */}
          <div className="col-span-2 bg-white border border-slate-200 rounded-xl p-6">
            <div className="flex justify-between items-center mb-5">
              <h2 className="text-lg font-semibold text-slate-900">Exposure by Country</h2>
              <div className="flex gap-2">
                <button className="p-1.5 hover:bg-slate-100 rounded">
                  <svg className="w-[18px] h-[18px] text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                </button>
              </div>
            </div>
            <div className="h-[280px] bg-slate-50 rounded-lg flex items-end p-5 mb-4">
              <div className="flex items-end gap-4 h-[200px] flex-1">
                <div className="flex-1 relative" style={{ height: '85%' }}>
                  <div className="w-full h-full bg-gradient-to-t from-blue-800 to-blue-500 rounded-t"></div>
                  <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-semibold text-slate-900 whitespace-nowrap">$18.4M</span>
                  <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[11px] text-slate-600 whitespace-nowrap">Vietnam</span>
                </div>
                <div className="flex-1 relative" style={{ height: '72%' }}>
                  <div className="w-full h-full bg-gradient-to-t from-blue-800 to-blue-500 rounded-t"></div>
                  <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-semibold text-slate-900 whitespace-nowrap">$15.2M</span>
                  <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[11px] text-slate-600 whitespace-nowrap">China</span>
                </div>
                <div className="flex-1 relative" style={{ height: '45%' }}>
                  <div className="w-full h-full bg-gradient-to-t from-blue-800 to-blue-500 rounded-t"></div>
                  <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-semibold text-slate-900 whitespace-nowrap">$9.1M</span>
                  <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[11px] text-slate-600 whitespace-nowrap">Bangladesh</span>
                </div>
                <div className="flex-1 relative" style={{ height: '28%' }}>
                  <div className="w-full h-full bg-gradient-to-t from-blue-800 to-blue-500 rounded-t"></div>
                  <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-semibold text-slate-900 whitespace-nowrap">$3.2M</span>
                  <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[11px] text-slate-600 whitespace-nowrap">Mexico</span>
                </div>
                <div className="flex-1 relative" style={{ height: '18%' }}>
                  <div className="w-full h-full bg-gradient-to-t from-blue-800 to-blue-500 rounded-t"></div>
                  <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-semibold text-slate-900 whitespace-nowrap">$1.3M</span>
                  <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[11px] text-slate-600 whitespace-nowrap">Ethiopia</span>
                </div>
              </div>
            </div>
            <div className="flex gap-5 text-xs">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-blue-800 rounded-sm"></div>
                <span>Current Exposure</span>
              </div>
            </div>
          </div>

          {/* Supplier Concentration */}
          <div className="bg-white border border-slate-200 rounded-xl p-6">
            <div className="flex justify-between items-center mb-5">
              <h2 className="text-lg font-semibold text-slate-900">Supplier Concentration</h2>
            </div>
            <div className="w-[200px] h-[200px] mx-auto mb-5 relative">
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center">
                <div className="text-[28px] font-bold text-slate-900">Top 5</div>
                <div className="text-xs text-slate-600">Suppliers</div>
              </div>
            </div>
            <div className="flex flex-col gap-3">
              <div className="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
                <span className="font-medium text-slate-900">Apex Manufacturing</span>
                <span className="font-semibold text-blue-700">$12.8M</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
                <span className="font-medium text-slate-900">Global Footwear Co.</span>
                <span className="font-semibold text-blue-700">$9.4M</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
                <span className="font-medium text-slate-900">Pacific Textiles Ltd.</span>
                <span className="font-semibold text-blue-700">$7.2M</span>
              </div>
            </div>
          </div>
        </div>

        {/* Top Material Alerts */}
        <div className="bg-white border border-slate-200 rounded-xl p-6">
          <div className="flex justify-between items-center mb-5">
            <h2 className="text-lg font-semibold text-slate-900">Top Material Alerts Requiring Executive Attention</h2>
            <div className="flex gap-2">
              <button className="p-1.5 hover:bg-slate-100 rounded">
                <svg className="w-[18px] h-[18px] text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
              </button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-600 uppercase tracking-wide border-b border-slate-200">Alert ID</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-600 uppercase tracking-wide border-b border-slate-200">Event</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-600 uppercase tracking-wide border-b border-slate-200">Severity</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-600 uppercase tracking-wide border-b border-slate-200">Exposure</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-600 uppercase tracking-wide border-b border-slate-200">Affected</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-600 uppercase tracking-wide border-b border-slate-200">Owner</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-600 uppercase tracking-wide border-b border-slate-200">Status</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-600 uppercase tracking-wide border-b border-slate-200">Days Open</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-slate-600 uppercase tracking-wide border-b border-slate-200">Action</th>
                </tr>
              </thead>
              <tbody>
                {alerts.map((alert) => (
                  <tr key={alert.id} className="hover:bg-slate-50">
                    <td className="py-4 px-4 text-sm text-slate-900 border-b border-slate-100"><strong>{alert.id}</strong></td>
                    <td className="py-4 px-4 text-sm text-slate-900 border-b border-slate-100">{alert.event}</td>
                    <td className="py-4 px-4 text-sm border-b border-slate-100">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-semibold ${
                        alert.severity === 'critical' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'
                      }`}>
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {alert.severity === 'critical' ? 'Critical' : 'High'}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-sm border-b border-slate-100"><strong>{alert.exposure}</strong></td>
                    <td className="py-4 px-4 text-sm text-slate-900 border-b border-slate-100">{alert.affected}</td>
                    <td className="py-4 px-4 text-sm text-slate-900 border-b border-slate-100">{alert.owner}</td>
                    <td className="py-4 px-4 text-sm border-b border-slate-100">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-medium ${
                        alert.status === 'unresolved' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'
                      }`}>
                        {alert.status === 'unresolved' ? 'Unresolved' : 'In Progress'}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-sm text-slate-900 border-b border-slate-100">{alert.days_open}</td>
                    <td className="py-4 px-4 text-sm border-b border-slate-100">
                      <Link to={`/alerts/${alert.id}`} className="text-blue-700 font-medium hover:underline">View Details →</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
