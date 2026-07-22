import { useEffect, useState } from 'react';
import { request } from '../lib/api-client';

interface PolicyEvent {
  id: string;
  date: string;
  effective_date: string;
  title: string;
  description: string;
  severity: string;
  policy_type: string;
  impact: string;
}

export default function PolicyMonitoringTimeline() {
  const [events, setEvents] = useState<PolicyEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchEvents() {
      try {
        setLoading(true);
        const response = await request<{ items: PolicyEvent[]; total: number } | PolicyEvent[]>('/policy-events');
        const items = Array.isArray(response) ? response : response?.items || [];
        
        // Mock data
        setEvents([
          {
            id: '1',
            date: 'Jan 15, 2026',
            effective_date: 'Feb 1, 2026',
            title: 'Vietnam Tariff Rate Increase on Footwear Imports',
            description: 'US Customs announced tariff rate increase from 15% to 22% for footwear imports (HTS 6403, 6404) from Vietnam. Affects 142 SKUs with estimated annual impact of $8.4M. Policy change driven by trade balance concerns and domestic manufacturing protection measures.',
            severity: 'critical',
            policy_type: 'Tariff Rate Change',
            impact: '$8.4M Impact'
          },
          {
            id: '2',
            date: 'Jan 8, 2026',
            effective_date: 'Feb 15, 2026',
            title: 'China Section 301 Tariff Expansion',
            description: 'USTR expanded Section 301 tariffs to include additional textile and apparel categories from China. New 25% tariff applies to synthetic fabric imports (HTS 5407, 5408). Affects 87 SKUs with estimated impact of $5.2M annually.',
            severity: 'high',
            policy_type: 'Tariff Rate Change',
            impact: '$5.2M Impact'
          }
        ]);
        setError(null);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch policy events');
      } finally {
        setLoading(false);
      }
    }
    fetchEvents();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading policy timeline...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-red-600 font-medium">Error: {error}</p>
          <button onClick={() => window.location.reload()} className="mt-4 px-4 py-2 bg-blue-700 text-white rounded-lg">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-50 min-h-screen">
      <div className="max-w-[1600px] mx-auto p-8">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 mb-6 text-sm text-slate-600">
          <a href="/" className="text-blue-700 hover:underline">Home</a>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
          <span>Policy Timeline</span>
        </div>

        {/* Page Header */}
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-[28px] font-bold text-slate-900 mb-2">Policy Monitoring Timeline</h1>
            <p className="text-sm text-slate-600">Track tariff and trade-policy changes affecting US import flows</p>
          </div>
          <div className="flex gap-3">
            <button className="flex items-center gap-2 px-5 py-2.5 border border-slate-200 bg-white text-slate-600 rounded-lg text-sm font-semibold hover:bg-slate-50">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              Advanced Filters
            </button>
            <button className="flex items-center gap-2 px-5 py-2.5 bg-blue-700 text-white rounded-lg text-sm font-semibold hover:bg-blue-800">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Export Timeline
            </button>
          </div>
        </div>

        {/* Filters Card */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 mb-6">
          <div className="flex gap-4 items-end">
            <div className="flex-1 flex flex-col gap-1.5">
              <label className="text-[13px] font-medium text-slate-600">Time Range</label>
              <select className="py-2.5 px-3 border border-slate-200 rounded-md text-sm text-slate-900 bg-white">
                <option>Last 90 Days</option>
                <option>Last 30 Days</option>
                <option>Last 6 Months</option>
              </select>
            </div>
            <div className="flex-1 flex flex-col gap-1.5">
              <label className="text-[13px] font-medium text-slate-600">Severity</label>
              <select className="py-2.5 px-3 border border-slate-200 rounded-md text-sm text-slate-900 bg-white">
                <option>All Severities</option>
                <option>Critical</option>
                <option>High</option>
              </select>
            </div>
            <div className="flex-1 flex flex-col gap-1.5">
              <label className="text-[13px] font-medium text-slate-600">Policy Type</label>
              <select className="py-2.5 px-3 border border-slate-200 rounded-md text-sm text-slate-900 bg-white">
                <option>All Types</option>
                <option>Tariff Rate Change</option>
              </select>
            </div>
            <div className="flex-1 flex flex-col gap-1.5">
              <label className="text-[13px] font-medium text-slate-600">Geography</label>
              <select className="py-2.5 px-3 border border-slate-200 rounded-md text-sm text-slate-900 bg-white">
                <option>All Countries</option>
                <option>Vietnam</option>
                <option>China</option>
              </select>
            </div>
            <button className="flex items-center gap-2 px-5 py-2.5 border border-slate-200 bg-white text-slate-600 rounded-lg text-sm font-semibold hover:bg-slate-50">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              Apply
            </button>
          </div>
        </div>

        {/* Timeline Container */}
        <div className="bg-white border border-slate-200 rounded-xl p-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-xl font-semibold text-slate-900">Policy Events (Last 90 Days)</h2>
            <div className="flex gap-5 text-xs">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-red-600 rounded-full"></div>
                <span>Critical</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-amber-500 rounded-full"></div>
                <span>High</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <span>Medium</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-slate-600 rounded-full"></div>
                <span>Low</span>
              </div>
            </div>
          </div>

          {/* Timeline */}
          <div className="relative pl-10">
            <div className="absolute left-3.5 top-0 bottom-0 w-0.5 bg-slate-200"></div>
            
            {events.map((event) => (
              <div key={event.id} className="relative pb-10 last:pb-0">
                <div className={`absolute left-[-30px] top-1.5 w-4 h-4 rounded-full border-[3px] border-white ${
                  event.severity === 'critical' ? 'bg-red-600 shadow-[0_0_0_2px_#DC2626]' : 'bg-amber-500 shadow-[0_0_0_2px_#F59E0B]'
                }`}></div>
                
                <div className="bg-slate-50 rounded-lg p-5">
                  <div className="text-xs text-slate-600 font-medium mb-2">{event.date} • Effective: {event.effective_date}</div>
                  <h3 className="text-base font-semibold text-slate-900 mb-2">{event.title}</h3>
                  <p className="text-sm text-slate-600 leading-relaxed mb-3">{event.description}</p>
                  
                  <div className="flex flex-wrap gap-4 mb-3">
                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-semibold ${
                      event.severity === 'critical' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'
                    }`}>
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {event.severity === 'critical' ? 'Critical' : 'High'}
                    </span>
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-semibold bg-slate-200 text-slate-600">
                      {event.policy_type}
                    </span>
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-semibold bg-red-100 text-red-700">
                      {event.impact}
                    </span>
                  </div>
                  
                  <div className="flex gap-3">
                    <a href={`/alerts/${event.id}`} className="text-blue-700 font-medium text-[13px] flex items-center gap-1 hover:underline">
                      View Alert Details
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </a>
                    <a href={`/scenarios`} className="text-blue-700 font-medium text-[13px] flex items-center gap-1 hover:underline">
                      View Mitigation Options
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
