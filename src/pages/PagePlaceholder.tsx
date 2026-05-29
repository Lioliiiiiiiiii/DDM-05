/**
 * Generic empty page used for every route while the site is still a skeleton.
 * Content will be filled in later — this just confirms routing + layout work.
 */
export function PagePlaceholder({ title }: { title: string }) {
  return (
    <div className="mx-auto max-w-4xl px-8 py-12">
      <h1 className="text-3xl font-bold text-slate-100">{title}</h1>
      <p className="mt-3 text-sm text-slate-500">
        This page is part of the Digital Disruption Matrix — Edition 2026.
        Content coming soon.
      </p>
      <div className="mt-10 rounded-xl border border-dashed border-base-700 bg-base-900/40 p-10 text-center text-sm text-slate-600">
        Placeholder — nothing here yet.
      </div>
    </div>
  );
}
