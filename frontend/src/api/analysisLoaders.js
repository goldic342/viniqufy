import AnalysisService from "./AnalysisService";

export const analysisLoader = async ({ params }) => {
  const service = new AnalysisService();
  const result = await service.fetchAnalysis(params.taskId);

  return result.result;
};

export const analysisLoadingLoader = async ({ params }) => {
  const service = new AnalysisService();
  const result = await service.startAnalysis(params.playlistId);

  return [result.task_id, result.playlist_info];
};
