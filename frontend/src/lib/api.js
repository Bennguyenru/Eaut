// API client for CLO/PLO Assessment Platform
const API_BASE_URL = 'http://localhost:5001/api'

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      return data
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // Health check
  async healthCheck() {
    return this.request('/health')
  }

  // PLO endpoints
  async getPLOs() {
    return this.request('/plos')
  }

  async getPLO(id) {
    return this.request(`/plos/${id}`)
  }

  async createPLO(data) {
    return this.request('/plos', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updatePLO(id, data) {
    return this.request(`/plos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async deletePLO(id) {
    return this.request(`/plos/${id}`, {
      method: 'DELETE',
    })
  }

  // CLO endpoints
  async getCLOs() {
    return this.request('/clos')
  }

  async getCLO(id) {
    return this.request(`/clos/${id}`)
  }

  async createCLO(data) {
    return this.request('/clos', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateCLO(id, data) {
    return this.request(`/clos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async deleteCLO(id) {
    return this.request(`/clos/${id}`, {
      method: 'DELETE',
    })
  }

  // Assessment endpoints
  async uploadDocument(formData) {
    return this.request('/assessments/upload', {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    })
  }

  async getAssessments() {
    return this.request('/assessments')
  }

  async getAssessment(id) {
    return this.request(`/assessments/${id}`)
  }

  async assessDocument(documentId) {
    return this.request(`/assessments/${documentId}/assess`, {
      method: 'POST',
    })
  }

  // Summary endpoints
  async getOverallSummary() {
    return this.request('/summary/overall')
  }

  async getCLOSummary() {
    return this.request('/summary/clo')
  }

  async getPLOSummary() {
    return this.request('/summary/plo')
  }

  // Mapping endpoints
  async getCLOPLOMapping() {
    return this.request('/mappings/clo-plo')
  }

  async updateCLOPLOMapping(data) {
    return this.request('/mappings/clo-plo', {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }
}

// Create and export a singleton instance
const apiClient = new ApiClient()
export default apiClient

// Export individual methods for convenience
export const {
  healthCheck,
  getPLOs,
  getPLO,
  createPLO,
  updatePLO,
  deletePLO,
  getCLOs,
  getCLO,
  createCLO,
  updateCLO,
  deleteCLO,
  uploadDocument,
  getAssessments,
  getAssessment,
  assessDocument,
  getOverallSummary,
  getCLOSummary,
  getPLOSummary,
  getCLOPLOMapping,
  updateCLOPLOMapping,
} = apiClient

