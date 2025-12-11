import { Route, Routes } from "react-router";
import Auth from "../pages/auth";
import Layout from "../layout";
import Home from "../pages/home";
import History from "../pages/history";

export default function RoutesDeclarative() {
  return (
    <Routes>
      <Route path="/sign">
        {/* <Route path="/sign/in/*" Component={Auth} /> */}
        <Route path="in/*" Component={Auth} />
        {/* <Route path="/sign/up/*" Component={Auth} /> */}
        <Route path="up/*" Component={Auth} />
      </Route>

      <Route Component={Layout}>
        <Route path="/" Component={Home} />
        <Route path="/history" Component={History} />
      </Route>
    </Routes>
  );
}
