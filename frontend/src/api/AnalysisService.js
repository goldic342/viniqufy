import axios from "axios";

export default class AnalysisService {
  apiBaseUrl = "http://localhost:8000";

  async #getSpotifyAnalysisStatus(taskId) {
    const response = await axios.get(`${this.apiBaseUrl}/spotify/analysis_status`, {
      params: { task_id: taskId },
    });
    return response.data;
  }

  async #fetchSpotifyAnalysis(taskId) {
    const response = await axios.get(`${this.apiBaseUrl}/spotify/analysis_result`, {
      params: { task_id: taskId },
    });
    return response.data;
  }

  async getSpotifyAnalysis(spotifyId) {
    const response = await axios.post(`${this.apiBaseUrl}/spotify/analysis`, {
      spotify_id: spotifyId,
    });

    const taskId = response.data.task_id;
    return new Promise((resolve, reject) => {
      const intervalId = setInterval(async () => {
        const task_status = await this.#getSpotifyAnalysisStatus(taskId).catch((e) => {
          clearInterval(intervalId);
          return reject(e); // Stopping function
        });

        if (task_status && task_status.status === "completed") {
          clearInterval(intervalId);
          const analysis = await this.#fetchSpotifyAnalysis(taskId).catch((e) => reject(e));

          if (analysis) {
            resolve(analysis.result);
          }
        }
      }, 1500);
    });
  }
}
