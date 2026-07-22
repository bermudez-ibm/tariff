import { HashRouter, Routes, Route, useParams, Link } from 'react-router-dom';
import { AuthProvider } from './lib/auth-context';
import LoginPage from './components/auth/LoginPage';
import RequireAuth from './components/auth/RequireAuth';
import Layout from './components/layout/Layout';
import ExecutiveExposureDashboard from './pages/ExecutiveExposureDashboard';
import PolicyMonitoringTimeline from './pages/PolicyMonitoringTimeline';

function PlaceholderPage({ title }: { title: string }) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-4">{title}</h2>
      <p className="text-gray-600">This page is under development.</p>
    </div>
  );
}

function AlertDetailPage() {
  const { alertId } = useParams();

  return (
    <div className="bg-slate-50 min-h-screen">
      <div className="max-w-[1600px] mx-auto p-8">
        <div className="flex items-center gap-2 mb-6 text-sm text-slate-600">
          <Link to="/" className="text-blue-700 hover:underline">Home</Link>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
          <Link to="/alerts" className="text-blue-700 hover:underline">Alerts</Link>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
          <span>{alertId}</span>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-6 mb-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-[28px] font-bold text-slate-900">{alertId}</h1>
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-semibold bg-red-100 text-red-700">
                  Critical
                </span>
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-medium bg-amber-100 text-amber-700">
                  Unresolved
                </span>
              </div>
              <h2 className="text-xl text-slate-700 mb-2">Vietnam Tariff Rate Increase on Footwear Imports</h2>
              <p className="text-sm text-slate-600">Created Jan 15, 2026 • Effective Date: Feb 1, 2026 • 12 days open</p>
            </div>
            <div className="flex gap-2">
              <button className="px-4 py-2 border border-slate-200 bg-white text-slate-700 rounded-lg text-sm font-semibold hover:bg-slate-50">
                Assign
              </button>
              <button className="px-4 py-2 bg-blue-700 text-white rounded-lg text-sm font-semibold hover:bg-blue-800">
                Mark Resolved
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-4 gap-5 mb-6">
          <div className="bg-white border border-slate-200 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-600 uppercase tracking-wide mb-2">Financial Impact</div>
            <div className="text-[32px] font-bold text-slate-900">$8.4M</div>
            <div className="text-[13px] text-slate-600">Annual exposure increase</div>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-600 uppercase tracking-wide mb-2">Affected Products</div>
            <div className="text-[32px] font-bold text-slate-900">142</div>
            <div className="text-[13px] text-slate-600">SKUs impacted</div>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-600 uppercase tracking-wide mb-2">Suppliers</div>
            <div className="text-[32px] font-bold text-slate-900">3</div>
            <div className="text-[13px] text-slate-600">Vietnamese factories</div>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-600 uppercase tracking-wide mb-2">Time to Effective</div>
            <div className="text-[32px] font-bold text-slate-900">4</div>
            <div className="text-[13px] text-slate-600">Days remaining</div>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-6 mb-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Policy Details</h3>
          <div className="space-y-3 text-sm">
            <div className="flex">
              <span className="w-40 font-medium text-slate-600">Policy Type:</span>
              <span className="text-slate-900">Tariff Rate Change</span>
            </div>
            <div className="flex">
              <span className="w-40 font-medium text-slate-600">Country:</span>
              <span className="text-slate-900">Vietnam</span>
            </div>
            <div className="flex">
              <span className="w-40 font-medium text-slate-600">HTS Codes:</span>
              <span className="text-slate-900">6403 (Leather Footwear), 6404 (Textile/Synthetic Footwear)</span>
            </div>
            <div className="flex">
              <span className="w-40 font-medium text-slate-600">Rate Change:</span>
              <span className="text-slate-900">15% → 22% (+7 percentage points)</span>
            </div>
            <div className="flex">
              <span className="w-40 font-medium text-slate-600">Owner:</span>
              <span className="text-slate-900">Strategic Sourcing Team</span>
            </div>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-6 mb-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Description</h3>
          <p className="text-sm text-slate-700 leading-relaxed">
            US Customs and Border Protection announced a tariff rate increase from 15% to 22% for footwear imports
            (HTS codes 6403, 6404) from Vietnam. The change affects 142 SKUs with an estimated annual impact of $8.4M.
            This policy change is driven by ongoing trade balance concerns and domestic manufacturing protection measures.
            The effective date is February 1, 2026, providing a limited window for mitigation actions.
          </p>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Recommended Mitigation Actions</h3>
          <div className="space-y-3">
            <div className="border border-slate-200 rounded-lg p-4 hover:bg-slate-50">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-semibold text-slate-900">Shift 50% Production to Bangladesh</h4>
                <span className="px-2.5 py-1 bg-emerald-100 text-emerald-700 text-xs font-semibold rounded-lg">
                  High Savings Potential
                </span>
              </div>
              <p className="text-sm text-slate-600 mb-3">
                Relocate half of affected production to existing Bangladesh suppliers. Bangladesh has 0% tariff under GSP.
              </p>
              <div className="flex gap-6 text-sm">
                <div>
                  <span className="text-slate-600">Savings:</span>
                  <span className="font-semibold text-slate-900"> $3.8M/year</span>
                </div>
                <div>
                  <span className="text-slate-600">Implementation:</span>
                  <span className="font-semibold text-slate-900"> 60-90 days</span>
                </div>
                <div>
                  <span className="text-slate-600">Complexity:</span>
                  <span className="font-semibold text-amber-700"> Medium</span>
                </div>
              </div>
            </div>

            <div className="border border-slate-200 rounded-lg p-4 hover:bg-slate-50">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-semibold text-slate-900">Negotiate Cost Absorption with Suppliers</h4>
                <span className="px-2.5 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded-lg">
                  Quick Win
                </span>
              </div>
              <p className="text-sm text-slate-600 mb-3">
                Request 3-4% price reduction from Vietnamese suppliers to offset tariff increase.
              </p>
              <div className="flex gap-6 text-sm">
                <div>
                  <span className="text-slate-600">Savings:</span>
                  <span className="font-semibold text-slate-900"> $2.1M/year</span>
                </div>
                <div>
                  <span className="text-slate-600">Implementation:</span>
                  <span className="font-semibold text-slate-900"> 14-30 days</span>
                </div>
                <div>
                  <span className="text-slate-600">Complexity:</span>
                  <span className="font-semibold text-emerald-700"> Low</span>
                </div>
              </div>
            </div>

            <div className="border border-slate-200 rounded-lg p-4 hover:bg-slate-50">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-semibold text-slate-900">Expand Mexico USMCA-Qualified Production</h4>
                <span className="px-2.5 py-1 bg-purple-100 text-purple-700 text-xs font-semibold rounded-lg">
                  Long-Term Strategy
                </span>
              </div>
              <p className="text-sm text-slate-600 mb-3">
                Move select high-value SKUs to Mexico to qualify for 0% USMCA duty-free benefits.
              </p>
              <div className="flex gap-6 text-sm">
                <div>
                  <span className="text-slate-600">Savings:</span>
                  <span className="font-semibold text-slate-900"> $1.9M/year</span>
                </div>
                <div>
                  <span className="text-slate-600">Implementation:</span>
                  <span className="font-semibold text-slate-900"> 90-120 days</span>
                </div>
                <div>
                  <span className="text-slate-600">Complexity:</span>
                  <span className="font-semibold text-red-700"> High</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <HashRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/"
            element={
              <RequireAuth>
                <Layout>
                  <ExecutiveExposureDashboard />
                </Layout>
              </RequireAuth>
            }
          />
          <Route
            path="/policy-events"
            element={
              <RequireAuth>
                <Layout>
                  <PolicyMonitoringTimeline />
                </Layout>
              </RequireAuth>
            }
          />
          <Route
            path="/scenarios"
            element={
              <RequireAuth>
                <Layout>
                  <PlaceholderPage title="Scenarios" />
                </Layout>
              </RequireAuth>
            }
          />
          <Route
            path="/agreements"
            element={
              <RequireAuth>
                <Layout>
                  <PlaceholderPage title="Trade Agreements" />
                </Layout>
              </RequireAuth>
            }
          />
          <Route
            path="/recommendations"
            element={
              <RequireAuth>
                <Layout>
                  <PlaceholderPage title="Recommendations" />
                </Layout>
              </RequireAuth>
            }
          />
          <Route
            path="/alerts"
            element={
              <RequireAuth>
                <Layout>
                  <PlaceholderPage title="Alerts" />
                </Layout>
              </RequireAuth>
            }
          />
          <Route
            path="/alerts/:alertId"
            element={
              <RequireAuth>
                <Layout>
                  <AlertDetailPage />
                </Layout>
              </RequireAuth>
            }
          />
          <Route
            path="/compliance"
            element={
              <RequireAuth>
                <Layout>
                  <PlaceholderPage title="Compliance" />
                </Layout>
              </RequireAuth>
            }
          />
        </Routes>
      </HashRouter>
    </AuthProvider>
  );
}

export default App;
