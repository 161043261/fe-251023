import { ClerkProvider } from "@clerk/clerk-react";

// react-router: Data
import { RouterProvider } from "react-router";
import router from "./router";

// react-router: Declarative
// import { BrowserRouter } from "react-router";
// import RoutesDeclarative from "./router/routes-declarative";

export default function App() {
  const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

  if (!PUBLISHABLE_KEY) {
    throw new Error("Missing Publishable Key");
  }
  return (
    <>
      <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
        <RouterProvider router={router} />
        {/* <BrowserRouter>
          <RoutesDeclarative />
        </BrowserRouter> */}
      </ClerkProvider>
    </>
  );
}
