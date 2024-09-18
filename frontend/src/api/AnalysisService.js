import axios from "axios";
import { json } from "react-router-dom";

// TODO: Add better error handling and validation in backend, and here so on
export default class AnalysisService {
  apiBaseUrl = "http://localhost:8000";

  async getAnalysisStatus(taskId) {
    const response = await axios.get(`${this.apiBaseUrl}/analysis/status`, {
      params: { task_id: taskId },
    });
    if (response.status !== 200) {
      throw json({ message: "Failed to fetch analysis result" }, { status: 500 });
    }
    return response.data;
  }

  async fetchAnalysis(taskId) {
    const response = await axios.get(`${this.apiBaseUrl}/analysis/result`, {
      params: { task_id: taskId },
    });

    if (response.status === 404) {
      throw json({ message: "There is not such task (¬_¬ )" }, { status: 404 });
    } else if (response.status === 500) {
      throw json(
        {
          message: "Internal error",
        },
        { status: 500 }
      );
    }

    return response.data;
  }

  async startAnalysis(spotifyId) {
    const response = await axios.post(`${this.apiBaseUrl}/analysis/start`, {
      spotify_playlist_id: spotifyId,
    });

    if (response.status !== 200) {
      throw json({ message: "Seems like this isn't playlist (￢_￢)" }, { status: 404 });
    }

    return response.data;
  }

  async pingAnalysisStatus(taskId) {
    return new Promise((resolve, reject) => {
      const intervalId = setInterval(async () => {
        try {
          const taskStatus = await this.getAnalysisStatus(taskId);

          // If task is completed, then resolve
          if (taskStatus && taskStatus.status === "SUCCESS") {
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
