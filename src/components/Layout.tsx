import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";

/**
 * App shell: the left sidebar and the top action bar are rendered here and
 * persist across every route. Page content is swapped into <Outlet />.
 */
export function Layout() {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-base-950">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar />
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
