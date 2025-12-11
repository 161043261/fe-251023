import { SignedIn, SignedOut, UserButton } from "@clerk/clerk-react";
import styles from "./index.module.scss";
import { Navigate, NavLink, Outlet } from "react-router";

export default function Layout() {
  return (
    <div className={styles["app-layout"]}>
      <header className={styles["app-header"]}>
        <div className={styles["header-content"]}>
          <h1>Code Problem Generator</h1>
          <nav>
            <SignedIn>
              <NavLink to="/">Generate Problem</NavLink>
              <NavLink to="/history">Generate History</NavLink>
              <UserButton />
            </SignedIn>
          </nav>
        </div>
      </header>

      <main className={styles["app-main"]}>
        <SignedOut>
          {/* It's recommended to avoid using this component in favor of useNavigate */}
          <Navigate to="/sign/in" replace />
        </SignedOut>

        <SignedIn>
          <Outlet />
        </SignedIn>
      </main>
    </div>
  );
}
