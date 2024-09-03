import AnalysisService from "./AnalysisService";

export const analysisLoader = async ({ params }) => {
  const service = new AnalysisService();
  const result = await service.fetchAnalysis(params.taskId);

  return result.result;
};
