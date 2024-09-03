import { createBrowserRouter, RouterProvider } from "react-router-dom";
import HomePage from "./pages/HomePage";
import AnalysisPage from "./pages/AnalysisPage";
import AnalysisLoadingPage from "./pages/AnalysisLoadingPage";
import { analysisLoader} from "./api/analysisLoaders";

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/analysis-loading/:playlistId",
    element: <AnalysisLoadingPage />,
  },
  {
    path: "/analysis/:taskId",
    element: <AnalysisPage />,
    loader: analysisLoader,
  },
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
