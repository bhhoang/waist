import React, { useState } from 'react';

function ExportData({ userName }) {
  const [exportStatus, setExportStatus] = useState(null);
  const [filters, setFilters] = useState({
    location: '',
    startDate: '',
    endDate: ''
  });

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const exportData = async (format) => {
    try {
      setExportStatus('exporting');
      
      // Build query parameters
      const params = new URLSearchParams();
      if (filters.location) params.append('location', filters.location);
      if (filters.startDate) params.append('start_date', filters.startDate);
      if (filters.endDate) params.append('end_date', filters.endDate);
      
      const queryString = params.toString();
      const url = `http://127.0.0.1:8000/export/${format}${queryString ? `?${queryString}` : ''}`;
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`Export failed: ${response.status}`);
      }
      
      // Get the blob and create download
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      
      // Extract filename from Content-Disposition header if available
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = `weather_export_${new Date().toISOString().split('T')[0]}.${format}`;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]*)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
      
      setExportStatus('success');
      setTimeout(() => setExportStatus(null), 3000);
    } catch (error) {
      console.error('Export error:', error);
      setExportStatus('error');
      setTimeout(() => setExportStatus(null), 3000);
    }
  };

  const exportFormats = [
    { format: 'json', label: 'JSON', description: 'JavaScript Object Notation' },
    { format: 'csv', label: 'CSV', description: 'Comma Separated Values' },
    { format: 'xml', label: 'XML', description: 'eXtensible Markup Language' }
  ];

  return (
    <div className="export-data" style={{ 
      border: '1px solid #ddd', 
      borderRadius: '8px', 
      padding: '20px', 
      margin: '20px 0',
      backgroundColor: '#f9f9f9'
    }}>
      <h3>Export Weather Data</h3>
      
      {/* Filter Controls */}
      <div style={{ marginBottom: '20px' }}>
        <h4>Filters (Optional)</h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Location:
              <input
                type="text"
                value={filters.location}
                onChange={(e) => handleFilterChange('location', e.target.value)}
                placeholder="Filter by location name"
                style={{ width: '100%', padding: '5px', marginTop: '2px' }}
              />
            </label>
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Start Date:
              <input
                type="date"
                value={filters.startDate}
                onChange={(e) => handleFilterChange('startDate', e.target.value)}
                style={{ width: '100%', padding: '5px', marginTop: '2px' }}
              />
            </label>
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              End Date:
              <input
                type="date"
                value={filters.endDate}
                onChange={(e) => handleFilterChange('endDate', e.target.value)}
                style={{ width: '100%', padding: '5px', marginTop: '2px' }}
              />
            </label>
          </div>
        </div>
      </div>

      {/* Export Buttons */}
      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '15px' }}>
        {exportFormats.map(({ format, label, description }) => (
          <button
            key={format}
            onClick={() => exportData(format)}
            disabled={exportStatus === 'exporting'}
            style={{
              padding: '10px 15px',
              backgroundColor: exportStatus === 'success' ? '#4CAF50' : exportStatus === 'error' ? '#f44336' : '#2196F3',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: exportStatus === 'exporting' ? 'not-allowed' : 'pointer',
              opacity: exportStatus === 'exporting' ? 0.6 : 1,
              minWidth: '100px'
            }}
            title={description}
          >
            {exportStatus === 'exporting' ? 'Exporting...' : 
             exportStatus === 'success' ? '✓ Done!' : 
             exportStatus === 'error' ? '✗ Error' : 
             `Export ${label}`}
          </button>
        ))}
      </div>

      {/* Status Messages */}
      {exportStatus === 'exporting' && (
        <p style={{ color: '#2196F3', fontSize: '0.9em' }}>
          🔄 Preparing export... This may take a moment.
        </p>
      )}
      {exportStatus === 'success' && (
        <p style={{ color: '#4CAF50', fontSize: '0.9em' }}>
          ✅ Export completed successfully! Check your downloads folder.
        </p>
      )}
      {exportStatus === 'error' && (
        <p style={{ color: '#f44336', fontSize: '0.9em' }}>
          ❌ Export failed. Please try again or contact support.
        </p>
      )}

      {/* Additional Export Options */}
      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#e8f4f8', borderRadius: '5px' }}>
        <h4 style={{ margin: '0 0 10px 0' }}>Quick Export Options</h4>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button
            onClick={() => exportData('locations/json')}
            disabled={exportStatus === 'exporting'}
            style={{
              padding: '8px 12px',
              backgroundColor: '#17a2b8',
              color: 'white',
              border: 'none',
              borderRadius: '3px',
              cursor: exportStatus === 'exporting' ? 'not-allowed' : 'pointer',
              fontSize: '0.9em'
            }}
          >
            Export Locations Only
          </button>
          <button
            onClick={() => exportData('weather/json')}
            disabled={exportStatus === 'exporting'}
            style={{
              padding: '8px 12px',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '3px',
              cursor: exportStatus === 'exporting' ? 'not-allowed' : 'pointer',
              fontSize: '0.9em'
            }}
          >
            Export Weather Only
          </button>
        </div>
      </div>
      
      <p style={{ fontSize: '0.8em', color: '#666', marginTop: '10px' }}>
        💡 Tip: Use filters to export specific data ranges or locations. 
        Leave filters empty to export all available data.
      </p>
    </div>
  );
}

export default ExportData;
