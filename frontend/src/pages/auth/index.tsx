import { SignedIn, SignedOut, SignIn, SignUp } from "@clerk/clerk-react";
import styles from "./index.module.scss";

export default function Auth() {
  return (
    <>
      <div className={styles["auth-container"]}>
        <SignedOut>
          <SignIn routing="path" path="/sign/in" />
          <SignUp routing="path" path="/sign/up" />
        </SignedOut>

        <SignedIn>
          <div className={styles["redirect-msg"]}>
            <p>You are already signed in.</p>
          </div>
        </SignedIn>
      </div>
    </>
  );
}
