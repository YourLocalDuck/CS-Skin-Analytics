import Loadable from "app/components/Loadable";
import { lazy } from "react";

const UpdateMarket = Loadable(lazy(() => import("app/views/market-actions/UpdateMarket")));

const marketActionsRoutes = [
    { path: "/marketactions/UpdateMarket", element: <UpdateMarket /> },
  ];
  
  export default marketActionsRoutes;