import type { RouteObject } from "react-router";
import Layout from "../layout";
import Auth from "../pages/auth";
import History from "../pages/history";
import Home from "../pages/home";

const routesData: RouteObject[] = [
  {
    // 前缀路由: 没有 Component 或 element 属性, 只提供统一的路由前缀
    path: "/sign",
    children: [
      {
        path: "in/*", // path: "/sign/in/*"
        Component: Auth,
      },
      {
        path: "up/*", // path: "/sign/up/*"
        Component: Auth,
      },
    ],
  },
  {
    // 布局路由: 没有 path 属性, 只提供统一的页面布局
    // path: "/",
    Component: Layout,
    children: [
      {
        // 索引路由: index: true, 即默认二级路由
        // index: true,
        path: "/",
        Component: Home,
      },
      {
        path: "/history",
        Component: History,
      },
    ],
  },
];

export default routesData;
