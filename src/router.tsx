import { createBrowserRouter } from "react-router-dom";
import { Layout } from "./components/Layout";
import { Home } from "./pages/Home";
import { PagePlaceholder } from "./pages/PagePlaceholder";
import { allRoutes } from "./navigation";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      ...allRoutes.map((route) => ({
        // strip the leading slash for the child route path
        path: route.path.replace(/^\//, ""),
        element: <PagePlaceholder title={route.label} />,
      })),
    ],
  },
]);
