export default function ResultCard({ title, data }) {
  if (!data) return null;
  return (
    <section className="card">
      <div className="card-header">
        <h3>{title}</h3>
      </div>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </section>
  );
}
