import sharedConfig from '../../../shared_config.json';

const baseUrl = import.meta.env.VITE_API_URL ?? `http://localhost:${sharedConfig.ports.backend}`;

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem(sharedConfig.auth.storage_key);
  const headers = new Headers(options.headers);
  
  if (token) {
    headers.set('Authorization', `${sharedConfig.auth.header_format.replace('{token}', token)}`);
  }
  
  if (options.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }
  
  const response = await fetch(
    `${baseUrl}${sharedConfig.api_base_path}${path}`,
    { ...options, headers }
  );
  
  if (response.status === 401) {
    localStorage.removeItem(sharedConfig.auth.storage_key);
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }
  
  if (!response.ok) {
    const errorText = await response.text().catch(() => 'Request failed');
    throw new Error(errorText || 'Request failed');
  }
  
  if (response.status === 204) {
    return null as T;
  }
  
  return response.json() as Promise<T>;
}
