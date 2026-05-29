/** Landing view shown at the root path. Intentionally minimal for now. */
export function Home() {
  return (
    <div className="mx-auto max-w-4xl px-8 py-16">
      <p className="text-sm font-semibold uppercase tracking-[0.25em] text-slate-500">
        Welcome to
      </p>
      <h1 className="mt-2 text-4xl font-extrabold leading-tight text-slate-100">
        Digital Disruption Matrix
        <span className="block text-2xl font-semibold text-slate-400">
          Edition 2026
        </span>
      </h1>
      <p className="mt-6 max-w-xl text-slate-400">
        Use the sidebar to explore by sector or by data, or jump straight to the
        key findings and the HeatMatrix from the top bar.
      </p>
    </div>
  );
}
