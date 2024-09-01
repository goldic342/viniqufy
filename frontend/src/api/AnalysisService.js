import axios from "axios";

export default class AnalysisService {
  apiBaseUrl = "http://localhost:8000";

  async getAnalysisStatus(taskId) {
    const response = await axios.get(`${this.apiBaseUrl}/spotify/analysis_status`, {
      params: { task_id: taskId },
    });
    return response.data;
  }

  async fetchAnalysis(taskId) {
    const response = await axios.get(`${this.apiBaseUrl}/spotify/analysis_result`, {
      params: { task_id: taskId },
    });
    return response.data;
  }

  async startAnalysis(spotifyId) {
    const response = await axios.post(`${this.apiBaseUrl}/spotify/analysis`, {
      spotify_id: spotifyId,
    });
    return response.data;
  }

  async pingAnalysisStatus(taskId) {
    return new Promise((resolve, reject) => {
      const intervalId = setInterval(async () => {
        try {
          const taskStatus = await this.getAnalysisStatus(taskId);

          // If task is completed, then resolve
          if (taskStatus && taskStatus.status === "completed") {
            clearInterval(intervalId);
            resolve(taskId);
          }
        } catch (error) {
          clearInterval(intervalId);
          reject(error);
        }
      }, 1500);
    });
  }
}
